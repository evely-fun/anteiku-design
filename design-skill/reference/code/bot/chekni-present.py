import asyncio
import logging
import time

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError, TelegramRetryAfter
from aiogram.types import InlineKeyboardMarkup, Message, ReactionTypeEmoji, ReplyParameters

from app.bot.report import Card
from app.config import get_settings
from app.core.store import KeyValueStore
from app.scanning.verdict import CLEAN, MALICIOUS, SUSPICIOUS, UNKNOWN

log = logging.getLogger(__name__)

EDIT_GAP = 1.4
RICH_OFF_KEY = "rich:off"
REACTIONS = {"scanning": "👀", CLEAN: "👌", SUSPICIOUS: "🤔", MALICIOUS: "😱", UNKNOWN: "🤷"}
EFFECT_CLEAN = "5107584321108051014"


class Presenter:
    def __init__(self, store: KeyValueStore) -> None:
        self._store = store
        self._last_edit: dict[tuple[int, int], float] = {}
        self.gap = EDIT_GAP

    async def rich_allowed(self) -> bool:
        return get_settings().rich_reports and not await self._store.get(RICH_OFF_KEY)

    async def _rich_failed(self, error: Exception) -> None:
        message = str(error).lower()
        if "rich" in message or "not found" in message or "unsupported" in message or "method" in message:
            await self._store.set(RICH_OFF_KEY, "1", ex=60 * 60)
        log.warning("rich_failed %s", error)

    async def react(self, bot: Bot, chat_id: int, message_id: int, state: str) -> None:
        emoji = REACTIONS.get(state)
        try:
            await bot.set_message_reaction(chat_id, message_id, reaction=[ReactionTypeEmoji(emoji=emoji)] if emoji else [])
        except (TelegramBadRequest, TelegramForbiddenError):
            pass
        except Exception as error:
            log.debug("reaction_failed %s", error)

    async def start(self, bot: Bot, chat_id: int, text: str, reply_to: int | None = None, thread_id: int | None = None) -> Message:
        return await bot.send_message(
            chat_id, text, message_thread_id=thread_id,
            reply_parameters=ReplyParameters(message_id=reply_to, allow_sending_without_reply=True) if reply_to else None,
        )

    async def update(self, message: Message, text: str) -> None:
        key = (message.chat.id, message.message_id)
        now = time.monotonic()
        if now - self._last_edit.get(key, 0) < self.gap:
            return
        self._last_edit[key] = now
        try:
            await message.edit_text(text)
        except TelegramRetryAfter as error:
            self._last_edit[key] = now + error.retry_after
        except TelegramBadRequest:
            pass

    async def finish(
        self, bot: Bot, message: Message, card: Card, markup: InlineKeyboardMarkup | None, effect: bool = False,
    ) -> Message | None:
        self._last_edit.pop((message.chat.id, message.message_id), None)
        if len(self._last_edit) > 5000:
            self._last_edit.clear()
        if effect and card.level == CLEAN and message.chat.type == "private":
            sent = await self.send(bot, message.chat.id, card, markup, reply_to=None, effect=EFFECT_CLEAN)
            if sent is not None:
                try:
                    await message.delete()
                except TelegramBadRequest:
                    pass
                return sent
        if await self.rich_allowed():
            try:
                result = await bot.edit_message_text(
                    chat_id=message.chat.id, message_id=message.message_id, rich_message=card.rich(), reply_markup=markup,
                )
                return result if isinstance(result, Message) else message
            except TelegramBadRequest as error:
                if "not modified" in str(error):
                    return message
                await self._rich_failed(error)
        try:
            result = await message.edit_text(card.plain(), reply_markup=markup)
            return result if isinstance(result, Message) else message
        except TelegramBadRequest as error:
            if "not modified" in str(error):
                return message
            log.warning("finish_failed %s", error)
            return await self.send(bot, message.chat.id, card, markup, reply_to=None)

    async def send(
        self, bot: Bot, chat_id: int, card: Card, markup: InlineKeyboardMarkup | None,
        reply_to: int | None = None, effect: str | None = None, thread_id: int | None = None,
    ) -> Message | None:
        reply = ReplyParameters(message_id=reply_to, allow_sending_without_reply=True) if reply_to else None
        if await self.rich_allowed():
            try:
                return await bot.send_rich_message(
                    chat_id, rich_message=card.rich(), reply_markup=markup, reply_parameters=reply,
                    message_effect_id=effect, message_thread_id=thread_id,
                )
            except TelegramBadRequest as error:
                await self._rich_failed(error)
        try:
            return await bot.send_message(
                chat_id, card.plain(), reply_markup=markup, reply_parameters=reply, message_effect_id=effect,
                message_thread_id=thread_id,
            )
        except (TelegramBadRequest, TelegramForbiddenError) as error:
            log.warning("send_failed %s", error)
            return None

    def forget_later(self, bot: Bot, chat_id: int, message_id: int, seconds: int) -> None:
        if seconds <= 0:
            return

        async def remove() -> None:
            await asyncio.sleep(seconds)
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception:
                pass

        asyncio.create_task(remove())
