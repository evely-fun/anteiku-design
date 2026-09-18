import hashlib
import json
import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeChat, FSInputFile, InputProfilePhotoStatic

from app.config import ASSETS, get_settings
from app.core.store import KeyValueStore

log = logging.getLogger(__name__)

NAME = "Анонка · анонимные вопросы"

SHORT_DESCRIPTION = (
    "Анонимные вопросы и сообщения от друзей. Ссылка в био, ответы в личку. Кто написал, не узнает никто."
)

DESCRIPTION = (
    "Получай анонимные сообщения от друзей и подписчиков.\n\n"
    "Жми «Начать», забирай свою ссылку и ставь её в био Telegram, TikTok или Instagram. "
    "Отвечай прямо тут, автор увидит ответ и останется анонимом.\n\n"
    "Кто написал, мы не показываем никому. Даже за деньги."
)

COMMANDS = [
    ("start", "Моя ссылка"),
    ("stats", "Статистика"),
    ("ask", "Вопрос на ссылке"),
    ("nick", "Свой адрес ссылки"),
    ("settings", "Настройки"),
    ("premium", "Premium"),
    ("help", "Как это работает"),
    ("support", "Поддержка"),
    ("terms", "Условия и конфиденциальность"),
]

CLEARED_LANGUAGES = ("en", "uk", "be", "kk", "uz")

ADMIN_COMMANDS = [
    ("admin", "Сводка"), ("reports", "Жалобы"), ("user", "Карточка u123"), ("staff", "Добавить админа u123"),
    ("broadcast", "Рассылка ответом"),
]

STAFF_COMMANDS = [("reports", "Жалобы")]


async def publish(bot: Bot, store: KeyValueStore) -> None:
    fingerprint = hashlib.sha256(
        json.dumps([NAME, SHORT_DESCRIPTION, DESCRIPTION, COMMANDS, ADMIN_COMMANDS, get_settings().admin_ids]).encode()
    ).hexdigest()
    if await store.get("profile:hash") != fingerprint:
        if await _texts(bot):
            await store.set("profile:hash", fingerprint)
    await _avatar(bot, store)


async def _texts(bot: Bot) -> bool:
    await bot.set_my_name(name=NAME)
    await bot.set_my_short_description(short_description=SHORT_DESCRIPTION)
    await bot.set_my_description(description=DESCRIPTION)
    await bot.set_my_commands(
        [BotCommand(command=command, description=text) for command, text in COMMANDS],
        scope=BotCommandScopeAllPrivateChats(),
    )
    for code in CLEARED_LANGUAGES:
        await bot.set_my_name(name="", language_code=code)
        await bot.set_my_short_description(short_description="", language_code=code)
        await bot.set_my_description(description="", language_code=code)
        await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats(), language_code=code)
    complete = True
    for admin_id in get_settings().admin_ids:
        try:
            await bot.set_my_commands(
                [BotCommand(command=command, description=text) for command, text in [*COMMANDS, *ADMIN_COMMANDS]],
                scope=BotCommandScopeChat(chat_id=admin_id),
            )
        except Exception:
            complete = False
    return complete


async def _avatar(bot: Bot, store: KeyValueStore) -> None:
    path = ASSETS / "covers" / "avatar.jpg"
    stamp = str(int(path.stat().st_mtime))
    if await store.get("profile:avatar") == stamp:
        return
    try:
        await bot.set_my_profile_photo(photo=InputProfilePhotoStatic(photo=FSInputFile(path)))
        await store.set("profile:avatar", stamp)
        log.info("bot_avatar_updated")
    except Exception as error:
        log.warning("bot_avatar_failed %s", error)


async def grant_staff_commands(bot: Bot, tg_id: int) -> None:
    try:
        await bot.set_my_commands(
            [BotCommand(command=command, description=text) for command, text in [*COMMANDS, *STAFF_COMMANDS]],
            scope=BotCommandScopeChat(chat_id=tg_id),
        )
    except Exception as error:
        log.info("staff_commands_failed %s", error)


async def revoke_staff_commands(bot: Bot, tg_id: int) -> None:
    try:
        await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=tg_id))
    except Exception as error:
        log.info("staff_commands_revoke_failed %s", error)
