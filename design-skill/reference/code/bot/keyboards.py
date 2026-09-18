from urllib.parse import quote

from aiogram.enums import ButtonStyle
from aiogram.types import (
    CopyTextButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    WebAppInfo,
)

from app.bot.texts import t
from app.config import get_settings
from app.db.models import User
from app.domain.users import link_for

REACTIONS = ("🔥", "❤", "🤣", "😱")
REACTION_LABELS = {"❤": "❤️"}


def miniapp_url(screen: str = "") -> str | None:
    settings = get_settings()
    if not settings.miniapp_enabled:
        return None
    base = settings.webapp_url.rstrip("/")
    return f"{base}/?screen={screen}" if screen else f"{base}/"


def menu_button(lang: str = "ru") -> MenuButtonWebApp | None:
    url = miniapp_url()
    if url is None:
        return None
    return MenuButtonWebApp(text=t(lang, "brand"), web_app=WebAppInfo(url=url))


def share_url(user: User, lang: str) -> str:
    link = link_for(user)
    return f"https://t.me/share/url?url={quote(link, safe='')}&text={quote(t(lang, 'share.text'), safe='')}"


def owner_menu(user: User, lang: str) -> InlineKeyboardMarkup:
    link = link_for(user)
    rows = [[InlineKeyboardButton(text=t(lang, "button.copy"), copy_text=CopyTextButton(text=link), style=ButtonStyle.PRIMARY)]]
    app = miniapp_url()
    if app is not None:
        rows.append([InlineKeyboardButton(text=t(lang, "button.app"), web_app=WebAppInfo(url=app), style=ButtonStyle.SUCCESS)])
    rows.append([InlineKeyboardButton(text=t(lang, "button.share"), url=share_url(user, lang))])
    story = miniapp_url("story")
    if story is not None:
        rows[-1].append(InlineKeyboardButton(text=t(lang, "button.story"), web_app=WebAppInfo(url=story)))
    rows.append([
        InlineKeyboardButton(text=t(lang, "button.prompt"), callback_data="prompt"),
        InlineKeyboardButton(text=t(lang, "button.settings"), callback_data="settings"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def cancel(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=t(lang, "button.cancel"), callback_data="cancel")]])


def after_send(lang: str, again: str | None, show_own: bool) -> InlineKeyboardMarkup | None:
    row = []
    if again:
        row.append(InlineKeyboardButton(text=t(lang, "button.again"), callback_data=f"again:{again}"))
    if show_own:
        row.append(InlineKeyboardButton(text=t(lang, "button.own"), callback_data="own", style=ButtonStyle.SUCCESS))
    return InlineKeyboardMarkup(inline_keyboard=[row]) if row else None


def incoming(public_id: str, lang: str, reaction: str = "", expanded: bool = False, blocked: bool = False) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=t(lang, "button.reply"), callback_data=f"r:{public_id}", style=ButtonStyle.PRIMARY)]]
    if not reaction:
        rows.append([
            InlineKeyboardButton(text=REACTION_LABELS.get(emoji, emoji), callback_data=f"x:{public_id}:{index}")
            for index, emoji in enumerate(REACTIONS)
        ])
    if expanded:
        rows.append([
            InlineKeyboardButton(
                text=t(lang, "button.unblock" if blocked else "button.block"),
                callback_data=f"{'u' if blocked else 'b'}:{public_id}",
                style=None if blocked else ButtonStyle.DANGER,
            ),
            InlineKeyboardButton(text=t(lang, "button.report"), callback_data=f"p:{public_id}"),
        ])
        rows.append([InlineKeyboardButton(text=t(lang, "button.back"), callback_data=f"k:{public_id}")])
    else:
        rows.append([InlineKeyboardButton(text=t(lang, "button.more"), callback_data=f"o:{public_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def settings_menu(user: User, lang: str) -> InlineKeyboardMarkup:
    def state(value: bool) -> str:
        return t(lang, "on" if value else "off")

    toggles = [
        ("paused", not user.paused),
        ("accept_media", user.accept_media),
        ("accept_links", user.accept_links),
        ("soft_filter", user.soft_filter),
        ("silent", user.silent),
    ]
    rows = [
        [InlineKeyboardButton(text=f"{t(lang, f'settings.{name}')}: {state(value)}", callback_data=f"set:{name}")]
        for name, value in toggles
    ]
    rows.append([InlineKeyboardButton(text=t(lang, "settings.lang"), callback_data="set:lang")])
    rows.append([
        InlineKeyboardButton(text=t(lang, "settings.nick"), callback_data="nick"),
        InlineKeyboardButton(text=t(lang, "settings.reset"), callback_data="reset"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def reset_confirm(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t(lang, "reset.yes"), callback_data="reset:yes", style=ButtonStyle.DANGER),
        InlineKeyboardButton(text=t(lang, "button.cancel"), callback_data="settings"),
    ]])


def prompt_menu(lang: str, has_prompt: bool) -> InlineKeyboardMarkup:
    rows = []
    if has_prompt:
        rows.append([InlineKeyboardButton(text=t(lang, "button.remove_prompt"), callback_data="prompt:clear")])
    rows.append([InlineKeyboardButton(text=t(lang, "button.cancel"), callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def premium_plans(lang: str, month: int, year: int, recurring: bool = False) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=t(lang, "premium.plan.month", stars=month), callback_data="pay:month", style=ButtonStyle.SUCCESS)],
        [InlineKeyboardButton(text=t(lang, "premium.plan.year", stars=year), callback_data="pay:year")],
    ]
    if recurring:
        rows.append([InlineKeyboardButton(text=t(lang, "premium.cancel"), callback_data="unsubscribe")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def stats_menu(lang: str, premium: bool) -> InlineKeyboardMarkup | None:
    rows = []
    app = miniapp_url("stats")
    if app is not None:
        rows.append([InlineKeyboardButton(text=t(lang, "button.app"), web_app=WebAppInfo(url=app))])
    if not premium:
        rows.append([InlineKeyboardButton(text=t(lang, "button.premium"), callback_data="premium")])
    return InlineKeyboardMarkup(inline_keyboard=rows) if rows else None


def age_menu(lang: str) -> InlineKeyboardMarkup:
    groups = ("u12", "13", "14", "16", "18")
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, f"age.{group}"), callback_data=f"age:{group}")] for group in groups
    ])


def report_reasons(public_id: str, lang: str) -> InlineKeyboardMarkup:
    reasons = ("harm", "intimate", "child", "spam", "other")
    rows = [[InlineKeyboardButton(text=t(lang, f"report.{reason}"), callback_data=f"q:{public_id}:{reason}")] for reason in reasons]
    rows.append([InlineKeyboardButton(text=t(lang, "button.back"), callback_data=f"o:{public_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def consent(plan: str, stars: int, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, f"premium.agree.{plan}", stars=stars), callback_data=f"agree:{plan}", style=ButtonStyle.SUCCESS)],
        [InlineKeyboardButton(text=t(lang, "button.cancel"), callback_data="cancel")],
    ])


def delete_confirm(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t(lang, "delete.yes"), callback_data="erase:yes", style=ButtonStyle.DANGER),
        InlineKeyboardButton(text=t(lang, "button.cancel"), callback_data="cancel"),
    ]])
