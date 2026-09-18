from html import escape

TEXTS: dict[str, dict[str, str]] = {
    "brand": {"ru": "Анонка", "en": "Anonka"},

    "owner.new": {
        "ru": (
            "<b>Твоя анонка готова</b>\n\n"
            "Кто откроет ссылку, сможет написать тебе анонимно. Кто именно написал, "
            "мы не показываем никому. Даже за деньги.\n\n"
            "{link}\n\n"
            "Закрепи её в био Telegram, TikTok или Instagram, так пишут чаще."
        ),
        "en": (
            "<b>Your Anonka is ready</b>\n\n"
            "Anyone who opens the link can message you anonymously. We never show who wrote, "
            "not to you and not for money.\n\n"
            "{link}\n\n"
            "Pin it in your Telegram, TikTok or Instagram bio, people write more that way."
        ),
    },
    "owner.back": {
        "ru": "<b>Твоя ссылка</b>\n\n{link}\n\nСегодня {visits} и {messages}.",
        "en": "<b>Your link</b>\n\n{link}\n\nToday: {visits} and {messages}.",
    },
    "owner.prompt": {"ru": "\n\nНа ссылке вопрос: <i>{prompt}</i>", "en": "\n\nQuestion on your link: <i>{prompt}</i>"},
    "owner.hint.empty": {
        "ru": "\n\nПока тихо. Кинь ссылку в сторис, обычно это работает.",
        "en": "\n\nQuiet so far. Drop the link in your story, that usually does it.",
    },

    "button.copy": {"ru": "Скопировать ссылку", "en": "Copy link"},
    "button.share": {"ru": "Отправить друзьям", "en": "Send to friends"},
    "button.story": {"ru": "Выложить в сторис", "en": "Post to story"},
    "button.app": {"ru": "Открыть анонку", "en": "Open Anonka"},
    "button.prompt": {"ru": "Вопрос на ссылке", "en": "Link question"},
    "button.settings": {"ru": "Настройки", "en": "Settings"},
    "button.cancel": {"ru": "Отмена", "en": "Cancel"},
    "button.back": {"ru": "Назад", "en": "Back"},
    "button.reply": {"ru": "Ответить", "en": "Reply"},
    "button.more": {"ru": "Ещё", "en": "More"},
    "button.block": {"ru": "Заблокировать", "en": "Block"},
    "button.unblock": {"ru": "Разблокировать", "en": "Unblock"},
    "button.report": {"ru": "Пожаловаться", "en": "Report"},
    "button.again": {"ru": "Написать ещё", "en": "Write again"},
    "button.own": {"ru": "Хочу свою ссылку", "en": "Get my own link"},
    "button.premium": {"ru": "Premium", "en": "Premium"},
    "button.remove_prompt": {"ru": "Убрать вопрос", "en": "Remove question"},

    "share.text": {
        "ru": "Напиши мне анонимно, я не узнаю, кто это",
        "en": "Message me anonymously, I won't know it's you",
    },

    "compose.open": {
        "ru": (
            "<b>Пишешь анонимно</b>\n\n"
            "Отправь текст, фото, видео, голосовое или кружок. Получатель не узнает, кто ты."
        ),
        "en": (
            "<b>You're writing anonymously</b>\n\n"
            "Send text, a photo, a video, a voice message or a video note. They won't know it's you."
        ),
    },
    "compose.prompt": {"ru": "<blockquote>{prompt}</blockquote>\n\n", "en": "<blockquote>{prompt}</blockquote>\n\n"},
    "compose.self": {
        "ru": "Это твоя же ссылка. Кинь её друзьям, и они смогут написать тебе.",
        "en": "That's your own link. Share it and your friends can write to you.",
    },
    "compose.gone": {
        "ru": "Ссылка не работает. Скорее всего, её обновили.",
        "en": "This link doesn't work anymore. It was probably changed.",
    },
    "compose.cancelled": {"ru": "Отменено.", "en": "Cancelled."},
    "reply.open": {
        "ru": "<b>Твой ответ</b>\n\nНапиши его одним сообщением. Можно текст, фото или голосовое.",
        "en": "<b>Your reply</b>\n\nSend it as one message. Text, a photo or a voice message all work.",
    },
    "reply.gone": {"ru": "Это сообщение уже недоступно.", "en": "This message is no longer available."},

    "sent": {"ru": "Отправлено. Ответ придёт сюда.", "en": "Sent. Replies will show up here."},
    "sent.reply": {"ru": "Ответ ушёл.", "en": "Reply sent."},

    "reject.self": {"ru": "Себе написать не получится.", "en": "You can't message yourself."},
    "reject.paused": {"ru": "Этот человек пока не принимает сообщения.", "en": "This person isn't taking messages right now."},
    "reject.blocked": {"ru": "Этот человек закрыл тебе переписку.", "en": "This person has closed the chat for you."},
    "reject.media_off": {"ru": "Тут принимают только текст.", "en": "Only text is accepted here."},
    "reject.links_off": {"ru": "Ссылки в сообщениях получатель отключил.", "en": "The recipient doesn't accept links."},
    "reject.rude": {
        "ru": "У получателя включён фильтр грубости. Перефразируй, и всё дойдёт.",
        "en": "The recipient has a rudeness filter on. Rephrase it and it'll go through.",
    },
    "reject.severe": {
        "ru": "Такое не отправится. Угрозы и призывы навредить себе тут под запретом.",
        "en": "This won't be sent. Threats and pushing someone to self-harm are not allowed here.",
    },
    "reject.too_long": {"ru": "Длинновато. Уложись в {limit} символов.", "en": "Too long. Keep it under {limit} characters."},
    "reject.unsupported": {
        "ru": "Такой формат не дойдёт. Можно текст, фото, видео, гиф, голосовое, кружок или стикер.",
        "en": "That format won't go through. Text, photo, video, GIF, voice, video note or sticker work.",
    },
    "reject.empty": {"ru": "Пустое сообщение не отправится.", "en": "An empty message can't be sent."},
    "reject.rate": {"ru": "Слишком часто. Подожди пару минут.", "en": "Too fast. Give it a couple of minutes."},
    "reject.pair": {
        "ru": "Этому человеку уже много сообщений. Дай время ответить.",
        "en": "That's a lot of messages for one person. Give them time to answer.",
    },
    "reject.unreachable": {
        "ru": "Не доставлено: получатель остановил бота.",
        "en": "Not delivered: the recipient has stopped the bot.",
    },
    "reject.banned": {
        "ru": "Отправка закрыта: аккаунт заблокирован за нарушения. Если это ошибка, напиши в поддержку.",
        "en": "Sending is closed: the account was banned for violations. If that's a mistake, contact support.",
    },
    "reject.gone": {"ru": "Это сообщение уже недоступно.", "en": "This message is no longer available."},
    "error": {
        "ru": "Что-то сломалось на нашей стороне. Попробуй ещё раз чуть позже.",
        "en": "Something broke on our side. Try again a bit later.",
    },
    "too.fast": {"ru": "Полегче, не так быстро.", "en": "Easy, not so fast."},

    "head.new": {"ru": "<b>Новое анонимное сообщение</b>", "en": "<b>New anonymous message</b>"},
    "head.follow": {"ru": "<b>Аноним ответил</b>", "en": "<b>Anonymous replied</b>"},
    "head.answer": {"ru": "<b>Тебе ответили</b>", "en": "<b>You got a reply</b>"},
    "head.source": {"ru": "\n<i>пришло из {source}</i>", "en": "\n<i>came from {source}</i>"},

    "reaction.notice": {"ru": "{emoji} на твоё сообщение отреагировали", "en": "{emoji} someone reacted to your message"},
    "reaction.saved": {"ru": "Реакция ушла", "en": "Reaction sent"},
    "block.done": {"ru": "Заблокировано. Этот автор больше не напишет", "en": "Blocked. They can't write to you anymore"},
    "block.undone": {"ru": "Разблокировано", "en": "Unblocked"},
    "report.done": {"ru": "Жалоба ушла, посмотрим в течение суток", "en": "Report sent, we'll check it within a day"},
    "report.dup": {"ru": "Жалоба уже отправлена", "en": "Already reported"},
    "fallback": {
        "ru": "Чтобы написать кому-то анонимно, открой его ссылку.\n\nА это твоя: {link}",
        "en": "To message someone anonymously, open their link.\n\nHere's yours: {link}",
    },

    "age.ask": {
        "ru": (
            "<b>Пара секунд до старта</b>\n\n"
            "Сколько тебе лет?\n\n"
            "Отвечая, ты принимаешь <a href=\"{terms}\">условия</a> и "
            "<a href=\"{privacy}\">политику конфиденциальности</a>."
        ),
        "en": (
            "<b>One second before we start</b>\n\n"
            "How old are you?\n\n"
            "By answering you accept the <a href=\"{terms}\">terms</a> and the "
            "<a href=\"{privacy}\">privacy policy</a>."
        ),
    },
    "age.u12": {"ru": "12 или меньше", "en": "12 or younger"},
    "age.13": {"ru": "13", "en": "13"},
    "age.14": {"ru": "14–15", "en": "14–15"},
    "age.16": {"ru": "16–17", "en": "16–17"},
    "age.18": {"ru": "18 и больше", "en": "18 or older"},
    "age.denied": {
        "ru": "Анонка доступна с {age} лет. Мы ничего о тебе не сохранили.",
        "en": "Anonka is available from age {age}. We haven't kept anything about you.",
    },

    "mydata.caption": {
        "ru": "Всё, что мы о тебе храним. Текст сообщений тут в открытом виде, не пересылай файл кому попало.",
        "en": "Everything we keep about you. Message text is in plain form here, so don't share the file.",
    },
    "delete.confirm": {
        "ru": (
            "<b>Удалить все данные?</b>\n\n"
            "Уйдут ссылка, настройки, статистика и все переписки с твоим участием, в том числе у собеседников. "
            "Отменить нельзя. Сообщения в чате с ботом останутся, их можно удалить самому.\n\n"
            "Записи об оплате хранятся отдельно, этого требует закон."
        ),
        "en": (
            "<b>Delete all your data?</b>\n\n"
            "Your link, settings, stats and every chat you took part in will be gone, including on the other side. "
            "This can't be undone. Messages in the bot chat stay, you can delete them yourself.\n\n"
            "Payment records are kept separately, as the law requires."
        ),
    },
    "delete.yes": {"ru": "Удалить навсегда", "en": "Delete forever"},
    "delete.done": {
        "ru": "Готово, данные удалены. Если напишешь боту снова, начнёшь с чистого листа.",
        "en": "Done, your data is deleted. If you write to the bot again, you start from scratch.",
    },
    "support.ask": {
        "ru": "<b>Поддержка</b>\n\nОпиши вопрос одним сообщением, ответим тут же, обычно в течение суток.",
        "en": "<b>Support</b>\n\nDescribe your question in one message, we reply right here, usually within a day.",
    },
    "support.sent": {"ru": "Обращение ушло. Ответ придёт в этот чат.", "en": "Sent. The reply will come to this chat."},
    "support.reply": {"ru": "<b>Ответ поддержки</b>\n\n{text}", "en": "<b>Support reply</b>\n\n{text}"},

    "report.ask": {"ru": "Что не так с сообщением?", "en": "What's wrong with this message?"},
    "report.harm": {"ru": "Угрозы или травля", "en": "Threats or bullying"},
    "report.intimate": {"ru": "Интимное без согласия", "en": "Intimate content without consent"},
    "report.child": {"ru": "Сексуальное с участием детей", "en": "Sexual content involving minors"},
    "report.spam": {"ru": "Спам или обман", "en": "Spam or scam"},
    "report.other": {"ru": "Другое", "en": "Something else"},
    "report.removed": {
        "ru": "Жалоба ушла, сообщение убрано из чата. Этот автор больше не сможет тебе писать.",
        "en": "Report sent and the message is removed from the chat. This sender can't write to you anymore.",
    },

    "premium.consent.month": {
        "ru": (
            "<b>Подписка Premium</b>\n\n"
            "{stars} ⭐ сразу и дальше каждые 30 дней, пока не отменишь. "
            "Отменить можно в любой момент командой /premium или в Telegram: Настройки, Мои звёзды, Подписки. "
            "После отмены Premium работает до конца оплаченного срока.\n\n"
            "Premium не раскрывает, кто написал."
        ),
        "en": (
            "<b>Premium subscription</b>\n\n"
            "{stars} ⭐ now and every 30 days until you cancel. "
            "Cancel any time with /premium or in Telegram: Settings, My Stars, Subscriptions. "
            "After cancelling, Premium works until the paid period ends.\n\n"
            "Premium never reveals who wrote."
        ),
    },
    "premium.consent.year": {
        "ru": "<b>Premium на год</b>\n\n{stars} ⭐ один раз, без автопродления.\n\nPremium не раскрывает, кто написал.",
        "en": "<b>Premium for a year</b>\n\n{stars} ⭐ once, no auto renewal.\n\nPremium never reveals who wrote.",
    },
    "premium.agree.month": {"ru": "Подписаться, {stars} ⭐ в месяц", "en": "Subscribe, {stars} ⭐ a month"},
    "premium.agree.year": {"ru": "Оплатить {stars} ⭐", "en": "Pay {stars} ⭐"},
    "premium.cancel": {"ru": "Отменить автопродление", "en": "Cancel auto renewal"},
    "premium.cancelled": {
        "ru": "Автопродление выключено. Premium работает до {date}.",
        "en": "Auto renewal is off. Premium works until {date}.",
    },
    "premium.nothing": {"ru": "Активной подписки нет.", "en": "No active subscription."},

    "settings.title": {
        "ru": "<b>Настройки</b>\n\nНажми на пункт, чтобы переключить.",
        "en": "<b>Settings</b>\n\nTap an item to switch it.",
    },
    "settings.paused": {"ru": "Приём сообщений", "en": "Taking messages"},
    "settings.accept_media": {"ru": "Фото, видео и голосовые", "en": "Photos, videos and voice"},
    "settings.accept_links": {"ru": "Ссылки в сообщениях", "en": "Links in messages"},
    "settings.soft_filter": {"ru": "Фильтр грубости", "en": "Rudeness filter"},
    "settings.silent": {"ru": "Уведомления без звука", "en": "Silent notifications"},
    "settings.lang": {"ru": "Язык: русский", "en": "Language: English"},
    "settings.nick": {"ru": "Свой адрес ссылки", "en": "Custom link"},
    "settings.reset": {"ru": "Новая ссылка", "en": "New link"},
    "on": {"ru": "вкл", "en": "on"},
    "off": {"ru": "выкл", "en": "off"},
    "saved": {"ru": "Сохранено", "en": "Saved"},

    "reset.confirm": {
        "ru": "Старая ссылка перестанет работать, свой адрес тоже сбросится. Обновить?",
        "en": "The old link will stop working and your custom address will be cleared. Continue?",
    },
    "reset.yes": {"ru": "Да, обновить", "en": "Yes, update"},
    "reset.done": {"ru": "<b>Ссылка обновлена</b>\n\n{link}\n\nСтарая больше не работает.", "en": "<b>Link updated</b>\n\n{link}\n\nThe old one no longer works."},

    "nick.ask": {
        "ru": (
            "<b>Свой адрес ссылки</b>\n\nСейчас: {link}\n\n"
            "Пришли адрес одним сообщением: латиница, цифры и _, от 4 до 24 символов."
        ),
        "en": (
            "<b>Custom link</b>\n\nNow: {link}\n\n"
            "Send the address in one message: latin letters, digits and _, 4 to 24 characters."
        ),
    },
    "nick.done": {"ru": "Готово, теперь ссылка такая:\n{link}", "en": "Done, your link is now:\n{link}"},
    "nick.format": {"ru": "Только латиница, цифры и _, от 4 до 24 символов.", "en": "Latin letters, digits and _ only, 4 to 24 characters."},
    "nick.reserved": {"ru": "Этот адрес занят системой, попробуй другой.", "en": "That address is reserved, try another one."},
    "nick.taken": {"ru": "Этот адрес уже кто-то забрал.", "en": "Someone already took that one."},

    "prompt.ask": {
        "ru": (
            "<b>Вопрос на ссылке</b>\n\n"
            "Его увидят все, кто откроет ссылку. Например: норм или стрём мой новый цвет волос?\n\n"
            "Пришли вопрос одним сообщением, до 140 символов."
        ),
        "en": (
            "<b>Link question</b>\n\n"
            "Everyone who opens your link will see it. For example: rate my new hair color?\n\n"
            "Send it in one message, up to 140 characters."
        ),
    },
    "prompt.done": {"ru": "Вопрос стоит на ссылке.", "en": "The question is on your link."},
    "prompt.removed": {"ru": "Вопрос убран.", "en": "Question removed."},
    "prompt.long": {"ru": "Длинновато, до 140 символов.", "en": "Too long, keep it under 140 characters."},

    "stats": {
        "ru": (
            "<b>Статистика</b>\n\n"
            "Переходы по ссылке: <b>{visits}</b>, за неделю {visits_week}\n"
            "Сообщения: <b>{messages}</b>, за неделю {messages_week}\n"
            "Твои ответы: <b>{replies}</b>"
        ),
        "en": (
            "<b>Stats</b>\n\n"
            "Link visits: <b>{visits}</b>, {visits_week} this week\n"
            "Messages: <b>{messages}</b>, {messages_week} this week\n"
            "Your replies: <b>{replies}</b>"
        ),
    },
    "stats.rank": {"ru": "\n\nПо сообщениям ты в топ {percent}% анонки.", "en": "\n\nBy messages you're in the top {percent}% of Anonka."},
    "stats.sources": {"ru": "\n\n<b>Откуда пишут</b>\n{lines}", "en": "\n\n<b>Where they come from</b>\n{lines}"},
    "stats.teaser": {
        "ru": "\n\nОткуда именно приходят люди, покажет Premium.",
        "en": "\n\nPremium shows exactly where people come from.",
    },

    "premium": {
        "ru": (
            "<b>Анонка Premium</b>\n\n"
            "• Метки для ссылок: видно, сколько пишут из Instagram, TikTok, Telegram и VK\n"
            "• Статистика за 30 дней с графиком\n"
            "• Шесть цветов карточки для сторис\n"
            "• Вся история сообщений в приложении, без срока\n\n"
            "Имя автора Premium не показывает. Анонимность не продаётся."
        ),
        "en": (
            "<b>Anonka Premium</b>\n\n"
            "• Link tags: see how many write from Instagram, TikTok, Telegram and VK\n"
            "• 30 day stats with a chart\n"
            "• Six colors for your story card\n"
            "• Your whole message history in the app, no expiry\n\n"
            "Premium never reveals who wrote. Anonymity is not for sale."
        ),
    },
    "premium.active": {"ru": "\n\nPremium работает до {date}.", "en": "\n\nPremium is active until {date}."},
    "premium.plan.month": {"ru": "Месяц · {stars} ⭐", "en": "Month · {stars} ⭐"},
    "premium.plan.year": {"ru": "Год · {stars} ⭐", "en": "Year · {stars} ⭐"},
    "premium.paid": {
        "ru": "<b>Premium включён</b>\n\nРаботает до {date}. Спасибо, что поддерживаешь анонку.",
        "en": "<b>Premium is on</b>\n\nActive until {date}. Thanks for supporting Anonka.",
    },
    "premium.failed": {"ru": "Оплата не прошла: {error}", "en": "Payment failed: {error}"},
    "pay.support": {
        "ru": "По вопросам оплаты пиши {contact}. Если Premium не заработал, вернём звёзды.",
        "en": "For payment questions write to {contact}. If Premium didn't work, we'll refund the stars.",
    },

    "help": {
        "ru": (
            "<b>Как это работает</b>\n\n"
            "Ты делишься ссылкой, люди пишут тебе анонимно, ты отвечаешь прямо тут. "
            "Автор увидит ответ и останется анонимом.\n\n"
            "Кто написал, мы не показываем. Даже за деньги.\n\n"
            "Если кто-то достаёт, жми «Ещё» под сообщением, там блок и жалоба. "
            "Угрозы и травлю разбираем и баним.\n\n"
            "Если тебе плохо или страшно, напиши тем, кому доверяешь, или позвони 112.\n\n"
            "/start твоя ссылка\n/nick свой адрес ссылки\n/ask вопрос на ссылке\n"
            "/stats статистика\n/settings настройки\n/premium Premium\n"
            "/support поддержка\n/mydata мои данные\n/deletedata удалить всё\n/terms условия"
        ),
        "en": (
            "<b>How it works</b>\n\n"
            "You share a link, people message you anonymously, you reply right here. "
            "They see your reply and stay anonymous.\n\n"
            "We never show who wrote. Not even for money.\n\n"
            "If someone bothers you, tap More under the message for block and report. "
            "Threats and bullying get reviewed and banned.\n\n"
            "If you feel unsafe, reach out to someone you trust or call 112.\n\n"
            "/start your link\n/nick custom link\n/ask link question\n"
            "/stats stats\n/settings settings\n/premium Premium\n"
            "/support support\n/mydata my data\n/deletedata delete everything\n/terms terms"
        ),
    },
    "legal": {
        "ru": "Условия: {terms}\nКонфиденциальность: {privacy}\nБезопасность и жалобы: {safety}",
        "en": "Terms: {terms}\nPrivacy: {privacy}\nSafety and reporting: {safety}",
    },
}

SOURCE_TITLES = {"ig": "Instagram", "tt": "TikTok", "tg": "Telegram", "vk": "VK", "": ""}

PLURALS = {
    "visit": {"ru": ("переход", "перехода", "переходов"), "en": ("visit", "visits", "visits")},
    "message": {"ru": ("сообщение", "сообщения", "сообщений"), "en": ("message", "messages", "messages")},
}


def t(lang: str, key: str, **values: object) -> str:
    entry = TEXTS.get(key)
    if entry is None:
        return key
    template = entry.get(lang) or entry["ru"]
    return template.format(**values) if values else template


def plural(lang: str, key: str, count: int) -> str:
    forms = PLURALS[key]["en" if lang == "en" else "ru"]
    if lang == "en":
        word = forms[0] if count == 1 else forms[1]
    else:
        tail = count % 100
        if 11 <= tail <= 14:
            word = forms[2]
        elif count % 10 == 1:
            word = forms[0]
        elif 2 <= count % 10 <= 4:
            word = forms[1]
        else:
            word = forms[2]
    return f"{count} {word}"


def safe(text: str) -> str:
    return escape(text, quote=False)
