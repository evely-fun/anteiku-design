import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import FSInputFile, InlineKeyboardMarkup, Message

from app.config import ASSETS
from app.core.store import KeyValueStore

log = logging.getLogger(__name__)

CAPTION_LIMIT = 1024


async def send_cover(
    bot: Bot,
    store: KeyValueStore,
    chat_id: int,
    name: str,
    caption: str,
    markup: InlineKeyboardMarkup | None = None,
    effect: str | None = None,
) -> Message:
    if len(caption) > CAPTION_LIMIT:
        return await bot.send_message(chat_id, caption, reply_markup=markup, message_effect_id=effect)
    key = f"cover:{name}"
    cached = await store.get(key)
    if cached:
        try:
            return await bot.send_photo(chat_id, cached, caption=caption, reply_markup=markup, message_effect_id=effect)
        except TelegramBadRequest:
            await store.delete(key)
    sent = await bot.send_photo(
        chat_id, FSInputFile(ASSETS / "covers" / f"{name}.jpg"), caption=caption, reply_markup=markup,
        message_effect_id=effect,
    )
    if sent.photo:
        await store.set(key, sent.photo[-1].file_id)
    return sent
