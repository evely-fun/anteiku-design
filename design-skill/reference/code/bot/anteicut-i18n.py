LANGUAGES = ("ru", "en")
DEFAULT = "ru"


def resolve(stored: str | None, telegram_code: str | None) -> str:
    return stored if stored in LANGUAGES else DEFAULT


TEXTS: dict[str, dict[str, str]] = {
    "start": {
        "ru": (
            "<b>Кидай ссылку, файл придёт сюда</b>\n\n"
            "TikTok, Reels, Shorts, YouTube, X, VK и ещё больше десятка площадок. "
            "Видео без водяных знаков, фото из каруселей, звук отдельным файлом.\n\n"
            "Нет ссылки? Напиши исполнителя и название, найду трек.\n\n"
            "Сегодня бесплатно {downloads}."
        ),
        "en": (
            "<b>Drop a link, the file lands here</b>\n\n"
            "TikTok, Reels, Shorts, YouTube, X, VK and a dozen more. "
            "Videos without watermarks, carousel photos, the sound as its own file.\n\n"
            "No link? Type the artist and the title, I'll find the track.\n\n"
            "Free today: {downloads}."
        ),
    },
    "start.premium": {
        "ru": "<b>Кидай ссылку, файл придёт сюда</b>\n\nPremium работает до {date}: без лимита, без очереди, до 4K.",
        "en": "<b>Drop a link, the file lands here</b>\n\nPremium is on until {date}: no limit, no queue, up to 4K.",
    },
    "start.button.app": {"ru": "Открыть приложение", "en": "Open the app"},
    "start.button.premium": {"ru": "Premium", "en": "Premium"},
    "start.button.help": {"ru": "Как это работает", "en": "How it works"},
    "help": {
        "ru": (
            "<b>Как это работает</b>\n\n"
            "Скопируй ссылку на пост и отправь сюда. Я покажу, что можно забрать: "
            "видео в нужном качестве, звук, фото, обложку или субтитры. Жмёшь кнопку, файл приходит в чат.\n\n"
            "Бесплатно {downloads} в день, видео до {height}p и не длиннее {minutes} минут. "
            "Premium снимает лимит и очередь и открывает качество до 4K.\n\n"
            "Формат звука меняется в /settings, остаток на сегодня покажет /limits."
        ),
        "en": (
            "<b>How it works</b>\n\n"
            "Copy a link to a post and send it here. I'll show what you can take: "
            "video in the quality you want, the sound, photos, the cover or subtitles. Tap a button, the file lands in the chat.\n\n"
            "Free: {downloads} a day, video up to {height}p and no longer than {minutes} minutes. "
            "Premium lifts the limit and the queue and opens quality up to 4K.\n\n"
            "Change the audio format in /settings, see what's left today with /limits."
        ),
    },
    "app.ready": {"ru": "В приложении есть превью и выбор кадров.", "en": "The app has previews and lets you pick frames."},
    "app.unavailable": {
        "ru": "Приложение сейчас не открывается. Кидай ссылку прямо в чат, работает так же.",
        "en": "The app won't open right now. Send the link straight to the chat, it works the same.",
    },
    "settings.title": {
        "ru": (
            "<b>Настройки</b>\n\n"
            "m4a приходит быстрее, звучит так же и играет прямо в Telegram. "
            "mp3 бери для старых плееров и магнитол.\n\n"
            "Площадка ниже ищет музыку, когда пишешь название трека."
        ),
        "en": (
            "<b>Settings</b>\n\n"
            "m4a arrives faster, sounds the same and plays right in Telegram. "
            "Pick mp3 for old players and car stereos.\n\n"
            "The source below is where I look when you type a track name."
        ),
    },
    "settings.format.m4a": {"ru": "m4a · быстрее", "en": "m4a · faster"},
    "settings.format.mp3": {"ru": "mp3 · играет везде", "en": "mp3 · plays anywhere"},
    "settings.saved": {"ru": "Сохранил", "en": "Saved"},
    "language.title": {"ru": "На каком языке говорим?", "en": "Which language do we speak?"},
    "language.saved": {"ru": "Теперь по-русски", "en": "English it is"},
    "searching": {"ru": "Ищу…", "en": "Looking…"},
    "downloading": {"ru": "Готовлю файл…", "en": "Getting the file ready…"},
    "search.result": {"ru": "Нашёл {tracks}. Какой нужен?", "en": "Found {tracks}. Which one?"},
    "search.empty": {
        "ru": "Ничего не нашёл. Добавь исполнителя, так точнее.",
        "en": "Nothing came up. Add the artist, it helps.",
    },
    "too.fast": {"ru": "Полегче, не успеваю за тобой. Секунду.", "en": "Easy, you're faster than me. One sec."},
    "track.expired": {"ru": "Список устарел, поищи ещё раз.", "en": "This list is stale, search again."},
    "collection": {"ru": "«{title}», {tracks}.", "en": "“{title}”, {tracks}."},
    "collection.truncated": {"ru": " Остальное пришли отдельной ссылкой.", "en": " Send the rest as a separate link."},
    "error.generic": {"ru": "Не вышло. Попробуй ещё раз через минуту.", "en": "That didn't work. Try again in a minute."},
    "media.looking": {"ru": "Смотрю, что там…", "en": "Checking the link…"},
    "media.choose": {"ru": "Что забираем?", "en": "What are we taking?"},
    "media.nothing": {
        "ru": "Тут нечего забрать: в посте нет ни видео, ни фото, ни звука.",
        "en": "Nothing to take here: the post has no video, photos or sound.",
    },
    "media.failed": {"ru": "Ссылка не открылась. Попробуй чуть позже.", "en": "The link didn't open. Try again a bit later."},
    "media.queued": {"ru": "Ставлю в очередь…", "en": "Queuing…"},
    "media.queue.position": {"ru": "В очереди перед тобой: {ahead}.", "en": "Ahead of you in the queue: {ahead}."},
    "media.queue.premium": {"ru": "\nС Premium очереди нет.", "en": "\nPremium skips the queue."},
    "media.starting": {"ru": "Начинаю…", "en": "Starting…"},
    "media.uploading": {"ru": "Отправляю в чат…", "en": "Sending it over…"},
    "media.progress": {"ru": "Качаю\n<code>{bar}</code> {percent}%{speed}", "en": "Downloading\n<code>{bar}</code> {percent}%{speed}"},
    "media.progress.plain": {"ru": "Качаю…", "en": "Downloading…"},
    "media.speed": {"ru": " · {speed} МБ/с", "en": " · {speed} MB/s"},
    "media.error": {"ru": "Не получилось скачать.", "en": "The download failed."},
    "media.working": {"ru": "Взял в работу", "en": "On it"},
    "banned": {"ru": "Доступ к боту закрыт.", "en": "Access to this bot is closed."},
    "quota.reached": {
        "ru": "На сегодня всё: {downloads} уже позади. Лимит обновится в {at}, а с Premium его нет совсем.",
        "en": "That's it for today: {downloads} done. The limit resets at {at}, and Premium has none at all.",
    },
    "quota.left": {
        "ru": "Сегодня осталось {left} из {limit}. Premium снимает лимит: /premium",
        "en": "{left} of {limit} left today. Premium lifts the limit: /premium",
    },
    "quota.premium": {
        "ru": "У тебя Premium: без лимита, без очереди и на полной скорости.",
        "en": "You have Premium: no limit, no queue, full speed.",
    },
    "premium.title": {"ru": "<b>AnteiCut Premium</b>", "en": "<b>AnteiCut Premium</b>"},
    "premium.perks": {
        "ru": (
            "• Качай сколько хочешь, без дневного лимита\n"
            "• Без очереди, даже вечером\n"
            "• Полная скорость сервера\n"
            "• YouTube до 4K и ролики до 4 часов"
        ),
        "en": (
            "• Download as much as you want, no daily limit\n"
            "• No queue, even in the evening\n"
            "• Full server speed\n"
            "• YouTube up to 4K and videos up to 4 hours"
        ),
    },
    "premium.active": {"ru": "Premium работает до {date}.", "en": "Premium is on until {date}."},
    "premium.left": {"ru": "Сегодня осталось {left} из {limit} бесплатных.", "en": "{left} of {limit} free downloads left today."},
    "premium.pick": {"ru": "Оплата звёздами Telegram.", "en": "Paid with Telegram Stars."},
    "premium.plan.month": {"ru": "Месяц · {stars} ⭐", "en": "Month · {stars} ⭐"},
    "premium.plan.quarter": {"ru": "3 месяца · {stars} ⭐", "en": "3 months · {stars} ⭐"},
    "premium.plan.year": {"ru": "Год · {stars} ⭐", "en": "Year · {stars} ⭐"},
    "premium.invoice.month": {
        "ru": "<b>Premium на месяц</b>\n\n{stars} ⭐ сейчас и дальше каждые 30 дней, пока не отменишь. Отменить можно в любой момент.",
        "en": "<b>Premium for a month</b>\n\n{stars} ⭐ now and every 30 days until you cancel. Cancel any time.",
    },
    "premium.invoice.quarter": {
        "ru": "<b>Premium на 3 месяца</b>\n\n{stars} ⭐ один раз, без автопродления.{saving}",
        "en": "<b>Premium for 3 months</b>\n\n{stars} ⭐ once, no auto renewal.{saving}",
    },
    "premium.invoice.year": {
        "ru": "<b>Premium на год</b>\n\n{stars} ⭐ один раз, без автопродления.{saving}",
        "en": "<b>Premium for a year</b>\n\n{stars} ⭐ once, no auto renewal.{saving}",
    },
    "premium.saving": {"ru": " Выходит на {percent}% дешевле, чем помесячно.", "en": " That's {percent}% less than paying monthly."},
    "premium.needed": {
        "ru": "Это открывается с Premium: 1080p и выше, длинные ролики, без лимита и очереди.",
        "en": "This opens with Premium: 1080p and up, long videos, no limit and no queue.",
    },
    "premium.open": {"ru": "Посмотреть Premium", "en": "See Premium"},
    "premium.pay": {"ru": "Оплатить {stars} ⭐", "en": "Pay {stars} ⭐"},
    "premium.paid": {
        "ru": "<b>Premium включён</b>\n\nРаботает до {date}. Спасибо, что поддерживаешь AnteiCut.{tail}",
        "en": "<b>Premium is on</b>\n\nActive until {date}. Thanks for backing AnteiCut.{tail}",
    },
    "premium.paid.subscription": {
        "ru": "\n\nПодписка продлевается сама. Отменить: Telegram, Настройки, Мои звёзды, Подписки.",
        "en": "\n\nThe subscription renews by itself. To cancel: Telegram, Settings, My Stars, Subscriptions.",
    },
    "premium.already": {"ru": "Premium уже работает до {date}.", "en": "Premium is already on until {date}."},
    "premium.failed": {"ru": "{error}\nНапиши в /paysupport, разберёмся.", "en": "{error}\nWrite to /paysupport and we'll sort it out."},
    "pay.check_failed": {"ru": "Не удалось проверить платёж, попробуй ещё раз.", "en": "Couldn't check the payment, try again."},
    "pay.support": {
        "ru": (
            "<b>Помощь с оплатой</b>\n\n"
            "Ответь на это сообщение: какой тариф, когда была оплата и что пошло не так. "
            "Проверим платёж и, если нужно, вернём звёзды.\n\n"
            "Отменить подписку: Telegram, Настройки, Мои звёзды, Подписки."
        ),
        "en": (
            "<b>Payment help</b>\n\n"
            "Reply to this message: which plan, when you paid and what went wrong. "
            "We'll check the payment and refund the stars if needed.\n\n"
            "To cancel a subscription: Telegram, Settings, My Stars, Subscriptions."
        ),
    },
    "queue.wait": {"ru": "Погоди, твои загрузки ещё идут.", "en": "Hold on, your downloads are still running."},
    "queue.full": {"ru": "Сейчас очень много загрузок. Попробуй через минуту.", "en": "It's very busy right now. Try again in a minute."},
    "error.unsupported": {"ru": "Эту ссылку я пока не умею скачивать.", "en": "I can't download this link yet."},
    "error.unavailable": {
        "ru": "Пост недоступен: удалён, закрыт или с ограничением по возрасту.",
        "en": "The post isn't available: deleted, private or age restricted.",
    },
    "error.drm": {
        "ru": "Трек защищён правообладателем, скачать его нельзя. Попробуй другую версию из списка.",
        "en": "This track is protected by the rights holder and can't be downloaded. Try another version from the list.",
    },
    "error.age_gated": {"ru": "Пост с возрастным ограничением, без входа его не открыть.", "en": "The post is age restricted and won't open without signing in."},
    "error.auth_required": {"ru": "Этот пост видно только после входа в аккаунт, скачать его не выйдет.", "en": "This post is only visible after signing in, so it can't be downloaded."},
    "error.blocked": {"ru": "Площадка сейчас не пускает нас к этому посту. Попробуй чуть позже.", "en": "The platform won't let us reach this post right now. Try again a bit later."},
    "error.throttled": {"ru": "Площадка попросила притормозить. Попробуй через пару минут.", "en": "The platform asked us to slow down. Try again in a couple of minutes."},
    "error.empty": {"ru": "В посте не нашлось видео или фото.", "en": "No video or photos in this post."},
    "error.too_large": {"ru": "Файл слишком большой для отправки в Telegram.", "en": "The file is too big to send through Telegram."},
    "error.network": {"ru": "Загрузка оборвалась. Попробуй ещё раз.", "en": "The download dropped. Try again."},
    "error.expired_source": {"ru": "Ссылка на файл устарела. Пришли пост ещё раз.", "en": "The file link expired. Send the post again."},
    "error.token_expired": {"ru": "Кнопки устарели. Пришли ссылку ещё раз.", "en": "These buttons expired. Send the link again."},
    "error.variant_missing": {"ru": "Такого качества больше нет. Пришли ссылку ещё раз.", "en": "That quality is gone. Send the link again."},
    "error.bot_blocked": {"ru": "Не могу тебе написать. Открой чат с ботом и нажми «Старт».", "en": "I can't message you. Open the chat with the bot and tap Start."},
}

PLURALS: dict[str, dict[str, tuple[str, ...]]] = {
    "download": {"ru": ("загрузка", "загрузки", "загрузок"), "en": ("download", "downloads")},
    "track": {"ru": ("трек", "трека", "треков"), "en": ("track", "tracks")},
}


def t(language: str, key: str, **kwargs) -> str:
    row = TEXTS.get(key) or {}
    text = row.get(language) or row.get(DEFAULT) or key
    return text.format(**kwargs) if kwargs else text


def plural(language: str, key: str, count: int) -> str:
    if language == "en":
        singular, many = PLURALS[key]["en"]
        return f"{count} {singular if count == 1 else many}"
    one, few, many = PLURALS[key]["ru"]
    tail = count % 100
    if 11 <= tail <= 14:
        word = many
    elif count % 10 == 1:
        word = one
    elif 2 <= count % 10 <= 4:
        word = few
    else:
        word = many
    return f"{count} {word}"


def has(key: str) -> bool:
    return key in TEXTS
