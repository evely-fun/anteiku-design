from dataclasses import dataclass

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, ReplyParameters

from app.bot import keyboards
from app.bot.texts import SOURCE_TITLES, safe, t

CAPTIONED = {"photo", "video", "animation", "voice", "audio"}
CAPTION_LIMIT = 1024
FIRST_MESSAGE_EFFECT = "5046509860389126442"


@dataclass(slots=True)
class Draft:
    kind: str
    text: str
    file_id: str
    chat_id: int
    message_id: int


@dataclass(slots=True)
class Envelope:
    chat_id: int
    lang: str
    head: str
    public_id: str
    silent: bool
    reply_to: int | None
    source: str = ""
    celebrate: bool = False


def _header(envelope: Envelope) -> str:
    head = t(envelope.lang, envelope.head)
    if envelope.source:
        head += t(envelope.lang, "head.source", source=SOURCE_TITLES.get(envelope.source, envelope.source))
    return head


def _reply(envelope: Envelope) -> ReplyParameters | None:
    if envelope.reply_to is None:
        return None
    return ReplyParameters(message_id=envelope.reply_to, allow_sending_without_reply=True)


async def deliver(bot: Bot, draft: Draft, envelope: Envelope) -> tuple[int, int | None]:
    header = _header(envelope)
    markup: InlineKeyboardMarkup = keyboards.incoming(envelope.public_id, envelope.lang)

    if draft.kind == "text":
        sent = await bot.send_message(
            envelope.chat_id,
            f"{header}\n\n{safe(draft.text)}",
            reply_markup=markup,
            disable_notification=envelope.silent,
            reply_parameters=_reply(envelope),
            message_effect_id=FIRST_MESSAGE_EFFECT if envelope.celebrate else None,
        )
        return sent.message_id, None

    caption = f"{header}\n\n{safe(draft.text)}" if draft.text else header
    if draft.kind in CAPTIONED and len(caption) <= CAPTION_LIMIT:
        sent = await bot.copy_message(
            envelope.chat_id,
            from_chat_id=draft.chat_id,
            message_id=draft.message_id,
            caption=caption,
            reply_markup=markup,
            disable_notification=envelope.silent,
            reply_parameters=_reply(envelope),
        )
        return sent.message_id, None

    copied = await bot.copy_message(
        envelope.chat_id,
        from_chat_id=draft.chat_id,
        message_id=draft.message_id,
        disable_notification=envelope.silent,
        reply_parameters=_reply(envelope),
    )
    sent = await bot.send_message(
        envelope.chat_id,
        header,
        reply_markup=markup,
        disable_notification=True,
        reply_parameters=ReplyParameters(message_id=copied.message_id, allow_sending_without_reply=True),
    )
    return sent.message_id, copied.message_id
