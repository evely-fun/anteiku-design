from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot import keyboards
from app.bot.covers import send_cover
from app.bot.texts import plural, safe, t
from app.context import AppContext
from app.db.models import User
from app.domain import stats
from app.domain.users import link_for

WELCOME_EFFECT = "5046509860389126442"


async def owner_caption(session: AsyncSession, user: User, created: bool) -> str:
    link = link_for(user)
    if created or (user.received_count == 0 and user.visits_count == 0):
        caption = t(user.lang, "owner.new", link=link)
    else:
        visits, messages = await stats.today(session, user)
        caption = t(
            user.lang, "owner.back", link=link,
            visits=plural(user.lang, "visit", visits), messages=plural(user.lang, "message", messages),
        )
        if user.received_count == 0:
            caption += t(user.lang, "owner.hint.empty")
    if user.prompt:
        caption += t(user.lang, "owner.prompt", prompt=safe(user.prompt))
    return caption


async def show_owner(bot: Bot, ctx: AppContext, session: AsyncSession, user: User, created: bool = False) -> None:
    caption = await owner_caption(session, user, created)
    await send_cover(
        bot, ctx.store, user.tg_id, "start", caption, keyboards.owner_menu(user, user.lang),
        effect=WELCOME_EFFECT if created else None,
    )


async def edit_or_send(callback: CallbackQuery, text: str, markup: InlineKeyboardMarkup | None) -> None:
    message = callback.message
    if message is None or message.photo or message.video or message.animation:
        await callback.bot.send_message(callback.from_user.id, text, reply_markup=markup)
        return
    try:
        await message.edit_text(text, reply_markup=markup)
    except TelegramBadRequest as error:
        if "not modified" not in error.message:
            await callback.bot.send_message(callback.from_user.id, text, reply_markup=markup)


async def swap_markup(callback: CallbackQuery, markup: InlineKeyboardMarkup | None) -> None:
    if callback.message is None:
        return
    try:
        await callback.message.edit_reply_markup(reply_markup=markup)
    except TelegramBadRequest:
        pass
