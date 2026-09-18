from html import escape

TEXTS: dict[str, dict[str, str]] = {
    "brand": {"ru": "Чекни", "en": "Chekni"},

    "start.new": {
        "ru": (
            "<b>Кидай файл, я проверю</b>\n\n"
            "Прогоню его через 70 с лишним антивирусов VirusTotal и свои проверки. "
            "Если файл уже встречался, ответ будет за секунду.\n\n"
            "Ещё умею:\n"
            "· ссылки и хэши, просто пришли текстом\n"
            "· QR-коды на картинках\n"
            "· охранять чаты и комментарии в каналах\n\n"
            "Сегодня доступно проверок: {left}."
        ),
        "en": (
            "<b>Drop a file, I'll check it</b>\n\n"
            "It goes through 70+ VirusTotal engines plus my own checks. "
            "If the file has been seen before, you get the answer in a second.\n\n"
            "I also check:\n"
            "· links and hashes, just send them as text\n"
            "· QR codes in pictures\n"
            "· group chats and channel comments\n\n"
            "Checks left today: {left}."
        ),
    },
    "start.back": {
        "ru": "<b>Кидай файл, ссылку или хэш</b>\n\nПроверено тобой: {scans}, угроз поймано: {threats}.\nСегодня доступно проверок: {left}.",
        "en": "<b>Send a file, a link or a hash</b>\n\nYou've checked {scans}, threats caught: {threats}.\nChecks left today: {left}.",
    },
    "start.invited": {
        "ru": "\n\nТебя позвал друг, вам обоим +{bonus} проверок.",
        "en": "\n\nA friend invited you, you both get +{bonus} checks.",
    },
    "invite.credited": {
        "ru": "По твоей ссылке пришёл человек. +{bonus} проверок, они не сгорают.",
        "en": "Someone joined with your link. +{bonus} checks, they never expire.",
    },

    "button.app": {"ru": "Открыть Чекни", "en": "Open Chekni"},
    "button.add_group": {"ru": "Добавить в чат", "en": "Add to a group"},
    "button.add_channel": {"ru": "Добавить в канал", "en": "Add to a channel"},
    "button.premium": {"ru": "Premium", "en": "Premium"},
    "button.settings": {"ru": "Настройки", "en": "Settings"},
    "button.invite": {"ru": "Позвать друга", "en": "Invite a friend"},
    "button.history": {"ru": "История", "en": "History"},
    "button.report": {"ru": "Отчёт VirusTotal", "en": "VirusTotal report"},
    "button.copy_hash": {"ru": "Скопировать SHA-256", "en": "Copy SHA-256"},
    "button.copy_link": {"ru": "Скопировать ссылку", "en": "Copy link"},
    "button.share": {"ru": "Переслать проверку", "en": "Share result"},
    "button.rescan": {"ru": "Перепроверить", "en": "Rescan"},
    "button.details": {"ru": "Подробнее", "en": "Details"},
    "button.in_app": {"ru": "Открыть отчёт", "en": "Open report"},
    "button.back": {"ru": "Назад", "en": "Back"},
    "button.cancel": {"ru": "Отмена", "en": "Cancel"},
    "button.close": {"ru": "Закрыть", "en": "Close"},
    "button.upload_anyway": {"ru": "Всё-таки загрузить", "en": "Upload anyway"},

    "stage.download": {"ru": "Скачиваю файл", "en": "Downloading"},
    "stage.hash": {"ru": "Считаю отпечаток", "en": "Fingerprinting"},
    "stage.lookup": {"ru": "Ищу в базах угроз", "en": "Searching threat databases"},
    "stage.upload": {"ru": "Файл новый, отправляю в VirusTotal", "en": "New file, sending it to VirusTotal"},
    "stage.analysis": {"ru": "Антивирусы смотрят", "en": "Engines are on it"},
    "stage.analysis.count": {"ru": "Антивирусы смотрят: {done} готово", "en": "Engines are on it: {done} done"},
    "progress.title.file": {"ru": "Проверяю файл", "en": "Checking the file"},
    "progress.title.url": {"ru": "Проверяю ссылку", "en": "Checking the link"},
    "progress.title.hash": {"ru": "Ищу хэш", "en": "Looking up the hash"},
    "progress.note": {
        "ru": "Новые файлы антивирусы смотрят до пары минут. Можно пока заняться своим, я пришлю ответ сюда.",
        "en": "New files take up to a couple of minutes. Feel free to do something else, the answer lands here.",
    },

    "level.clean": {"ru": "Чисто", "en": "Clean"},
    "level.suspicious": {"ru": "Есть сомнения", "en": "Looks suspicious"},
    "level.malicious": {"ru": "Опасно", "en": "Dangerous"},
    "level.unknown": {"ru": "Проверить до конца не вышло", "en": "Couldn't finish the check"},

    "summary.clean": {
        "ru": "Ни один из {total} антивирусов ничего не нашёл. Выглядит норм.",
        "en": "None of the {total} engines found anything. Looks clean.",
    },
    "summary.clean.trusted": {
        "ru": "Этот файл есть в базе проверенных программ NSRL, он известен и безопасен.",
        "en": "This file is in the NSRL database of known software, it's a known good file.",
    },
    "summary.suspicious": {
        "ru": "{hits} из {total} антивирусов насторожились. Открывай, только если доверяешь отправителю.",
        "en": "{hits} of {total} engines raised a flag. Only open it if you trust the sender.",
    },
    "summary.suspicious.signals": {
        "ru": "Антивирусы молчат, но с файлом что-то не так, смотри ниже. Открывай, только если доверяешь отправителю.",
        "en": "Engines are quiet, but something about the file is off, see below. Only open it if you trust the sender.",
    },
    "summary.malicious": {
        "ru": "{hits} из {total} антивирусов нашли угрозу. Не открывай этот файл и удали его.",
        "en": "{hits} of {total} engines found a threat. Don't open this file, delete it.",
    },
    "summary.malicious.intel": {
        "ru": "Файл есть в базах известных вредоносов. Не открывай его и удали.",
        "en": "The file is in known malware databases. Don't open it, delete it.",
    },
    "summary.url.clean": {
        "ru": "Ни один из {total} сервисов не считает ссылку опасной.",
        "en": "None of the {total} services flag this link.",
    },
    "summary.url.suspicious": {
        "ru": "{hits} из {total} сервисов насторожились. Не вводи там пароли и данные карты.",
        "en": "{hits} of {total} services raised a flag. Don't enter passwords or card details there.",
    },
    "summary.url.malicious": {
        "ru": "{hits} из {total} сервисов считают ссылку опасной. Не переходи по ней.",
        "en": "{hits} of {total} services mark this link as dangerous. Don't open it.",
    },
    "summary.unknown.private": {
        "ru": "Файл новый, в базах его нет. Загрузка в VirusTotal выключена в настройках, поэтому работали только локальные проверки.",
        "en": "The file is new and not in any database. Uploading to VirusTotal is off in your settings, so only local checks ran.",
    },
    "summary.unknown.quota": {
        "ru": "VirusTotal сейчас перегружен. Попробуй через пару минут.",
        "en": "VirusTotal is overloaded right now. Try again in a couple of minutes.",
    },
    "summary.unknown.media": {
        "ru": "Это картинка или видео. Такие файлы почти никогда не несут вирусов, поэтому я их не загружаю. Отпечатка в базах угроз нет.",
        "en": "It's a picture or a video. These almost never carry malware, so I don't upload them. The fingerprint isn't in any threat database.",
    },
    "summary.unknown.not_found": {
        "ru": "Такого хэша нет ни в VirusTotal, ни в базах вредоносов. Пришли сам файл, проверю его.",
        "en": "This hash isn't in VirusTotal or any malware database. Send the file itself and I'll check it.",
    },
    "summary.unknown.vt_off": {
        "ru": "Проверка через 70 антивирусов сейчас не подключена, поэтому смотрели только ClamAV и мои проверки маскировки. Угроз они не нашли, но совсем новые вирусы ClamAV может не знать.",
        "en": "The 70-engine check isn't connected right now, so only ClamAV and my disguise checks ran. They found nothing, but ClamAV may miss brand-new malware.",
    },
    "summary.unknown.off": {
        "ru": "Облачные проверки сейчас недоступны, сработали только локальные. Попробуй позже.",
        "en": "Cloud checks are unavailable right now, only local ones ran. Try again later.",
    },
    "local.clean": {"ru": "ClamAV тоже ничего не нашёл.", "en": "ClamAV found nothing either."},
    "threat.label": {"ru": "Угроза: <b>{threat}</b>", "en": "Threat: <b>{threat}</b>"},
    "detections.title": {"ru": "Кто что нашёл", "en": "What each engine found"},
    "hashes.title": {"ru": "Отпечатки", "en": "Hashes"},
    "notes.title": {"ru": "Что ещё заметил", "en": "What else I noticed"},
    "qr.title": {"ru": "На картинке QR-код со ссылкой", "en": "The picture has a QR code with a link"},
    "footer.checked": {"ru": "Проверено {date}", "en": "Checked {date}"},
    "footer.cached": {"ru": "ответ из базы", "en": "from cache"},
    "footer.uploaded": {"ru": "загружен в VirusTotal", "en": "uploaded to VirusTotal"},
    "footer.disclaimer": {
        "ru": "Проверка снижает риск, но не даёт гарантий.",
        "en": "A scan lowers the risk but can't guarantee anything.",
    },

    "row.file": {"ru": "Файл", "en": "File"},
    "row.link": {"ru": "Ссылка", "en": "Link"},
    "row.size": {"ru": "Размер", "en": "Size"},
    "row.type": {"ru": "Тип", "en": "Type"},
    "row.engines": {"ru": "Сработали", "en": "Detections"},
    "row.first_seen": {"ru": "Впервые замечен", "en": "First seen"},
    "row.lookups": {"ru": "Проверок у нас", "en": "Checks here"},
    "row.sources": {"ru": "Источники", "en": "Sources"},

    "signal.rtlo": {
        "ru": "В имени спрятан символ, который переворачивает текст. Так выдают программу за .pdf или .jpg",
        "en": "The name hides a character that flips text direction. That's how programs pose as .pdf or .jpg",
    },
    "signal.double_ext": {
        "ru": "Двойное расширение: файл притворяется документом, а на деле запускается",
        "en": "Double extension: the file pretends to be a document but actually runs",
    },
    "signal.padded_name": {
        "ru": "Настоящее расширение утоплено за пробелами в имени",
        "en": "The real extension is hidden behind spaces in the name",
    },
    "signal.disguised": {
        "ru": "Внутри программа, хотя расширение говорит об обычном файле",
        "en": "There's a program inside even though the extension says otherwise",
    },
    "signal.runnable": {
        "ru": "Это запускаемый файл, открывай его только из надёжного источника",
        "en": "This file runs code, only open it if it came from a source you trust",
    },
    "signal.disk_image": {
        "ru": "Образ диска. Через них часто обходят защиту Windows",
        "en": "Disk image. These are often used to slip past Windows protection",
    },
    "signal.macro": {"ru": "В документе есть макросы", "en": "The document contains macros"},
    "signal.pdf_active": {"ru": "В PDF есть скрипты или команды запуска", "en": "The PDF contains scripts or launch actions"},
    "signal.encrypted_archive": {
        "ru": "Архив под паролем, антивирусы не видят, что внутри",
        "en": "Password-protected archive, engines can't see inside",
    },
    "signal.archive_runnable": {"ru": "В архиве запускаемые файлы: {inner}", "en": "Runnable files inside: {inner}"},
    "signal.archive_unreadable": {
        "ru": "Архив устроен необычно, заглянуть внутрь без распаковки не вышло",
        "en": "The archive has an unusual structure, I couldn't look inside without unpacking it",
    },
    "signal.archive_double_ext": {
        "ru": "В архиве файл с двойным расширением",
        "en": "The archive has a file with a double extension",
    },

    "error.too_big.cloud": {
        "ru": "Файл весит {size}, а Telegram отдаёт ботам только до 20 МБ. Пришли хэш файла или ссылку на него, проверю так.",
        "en": "The file is {size}, and Telegram only lets bots download up to 20 MB. Send its hash or a link to it instead.",
    },
    "error.too_big.free": {
        "ru": "Файл весит {size}. Бесплатно проверяю до {limit}, с Premium до 2 ГБ.",
        "en": "The file is {size}. Free checks go up to {limit}, Premium goes up to 2 GB.",
    },
    "error.download": {
        "ru": "Не получилось скачать файл из Telegram. Пришли его ещё раз.",
        "en": "Couldn't download the file from Telegram. Send it again.",
    },
    "error.failed": {
        "ru": "Проверка сломалась на моей стороне. Попробуй ещё раз через минуту.",
        "en": "The check broke on my side. Try again in a minute.",
    },
    "error.quota": {
        "ru": "На сегодня проверки закончились: {limit} из {limit}. Завтра снова будут, а с Premium их 400 в день.",
        "en": "You're out of checks for today: {limit} of {limit}. More tomorrow, or 400 a day with Premium.",
    },
    "error.lookups": {
        "ru": "Слишком много запросов за день. Продолжим завтра.",
        "en": "Too many lookups today. Let's continue tomorrow.",
    },
    "error.busy": {
        "ru": "Этот файл уже проверяется, дождись ответа выше.",
        "en": "This file is already being checked, wait for the answer above.",
    },
    "error.rescan_cooldown": {
        "ru": "Перепроверять можно раз в 10 минут.",
        "en": "You can rescan once every 10 minutes.",
    },
    "error.premium_only": {
        "ru": "Перепроверка есть в Premium.",
        "en": "Rescanning is a Premium feature.",
    },
    "error.gone": {"ru": "Эта проверка больше не хранится.", "en": "This check is no longer stored."},
    "error.generic": {"ru": "Что-то пошло не так, попробуй ещё раз.", "en": "Something went wrong, try again."},
    "too.fast": {"ru": "Слишком часто. Подожди пару секунд.", "en": "Too fast. Give it a couple of seconds."},
    "banned": {"ru": "Доступ к боту закрыт.", "en": "Access to the bot is closed."},

    "text.nothing": {
        "ru": "Пришли файл, ссылку или хэш (MD5, SHA-1, SHA-256), и я проверю.",
        "en": "Send a file, a link or a hash (MD5, SHA-1, SHA-256) and I'll check it.",
    },
    "photo.no_qr": {
        "ru": "На картинке нет QR-кода со ссылкой. Сами картинки вирусов почти не несут. Если нужно проверить именно файл, пришли его документом.",
        "en": "No QR code with a link in this picture. Pictures themselves almost never carry malware. To check the exact file, send it as a document.",
    },
    "links.many": {"ru": "Проверяю ссылки: {count}", "en": "Checking links: {count}"},

    "settings.title": {
        "ru": "<b>Настройки</b>\n\nЕсли файла нет ни в одной базе, я загружаю его в VirusTotal. Там его увидят исследователи безопасности. Личные документы лучше не присылать или выключить загрузку.",
        "en": "<b>Settings</b>\n\nIf a file isn't in any database, I upload it to VirusTotal, where security researchers can see it. Don't send private documents, or turn uploading off.",
    },
    "settings.share_unknown": {"ru": "Загружать новые файлы в VirusTotal", "en": "Upload new files to VirusTotal"},
    "settings.effects": {"ru": "Анимации в ответах", "en": "Animations in replies"},
    "settings.lang": {"ru": "Язык: русский", "en": "Language: English"},
    "on": {"ru": "вкл", "en": "on"},
    "off": {"ru": "выкл", "en": "off"},

    "premium": {
        "ru": (
            "<b>Чекни Premium</b>\n\n"
            "· 400 файлов в день вместо 25\n"
            "· файлы до 2 ГБ\n"
            "· перепроверка свежими базами\n"
            "· твои файлы идут первыми, когда VirusTotal занят\n"
            "· история проверок без срока\n\n"
            "Деньги идут на серверы и ключи антивирусных баз."
        ),
        "en": (
            "<b>Chekni Premium</b>\n\n"
            "· 400 files a day instead of 25\n"
            "· files up to 2 GB\n"
            "· rescans with fresh databases\n"
            "· your files go first when VirusTotal is busy\n"
            "· unlimited check history\n\n"
            "The money pays for servers and threat database keys."
        ),
    },
    "premium.active": {"ru": "\n\nPremium активен до {date}.", "en": "\n\nPremium is active until {date}."},
    "premium.plan.month": {"ru": "Месяц · {stars} ⭐", "en": "Month · {stars} ⭐"},
    "premium.plan.year": {"ru": "Год · {stars} ⭐", "en": "Year · {stars} ⭐"},
    "premium.cancel": {"ru": "Отменить продление", "en": "Cancel renewal"},
    "premium.consent.month": {
        "ru": "<b>Подписка на месяц</b>\n\n{stars} ⭐ списываются сейчас и потом каждые 30 дней, пока не отменишь. Отменить можно в любой момент здесь или в настройках Telegram, оплаченный срок сохранится.\n\nНажимая кнопку, ты соглашаешься с условиями: /terms",
        "en": "<b>Monthly subscription</b>\n\n{stars} ⭐ now and every 30 days until you cancel. Cancel any time here or in Telegram settings, the paid period stays.\n\nBy tapping the button you accept the terms: /terms",
    },
    "premium.consent.year": {
        "ru": "<b>Premium на год</b>\n\n{stars} ⭐ один раз, без автопродления.\n\nНажимая кнопку, ты соглашаешься с условиями: /terms",
        "en": "<b>Premium for a year</b>\n\n{stars} ⭐ once, no auto-renewal.\n\nBy tapping the button you accept the terms: /terms",
    },
    "premium.agree.month": {"ru": "Подписаться за {stars} ⭐", "en": "Subscribe for {stars} ⭐"},
    "premium.agree.year": {"ru": "Оплатить {stars} ⭐", "en": "Pay {stars} ⭐"},
    "premium.paid": {"ru": "Premium включён до {date}. Спасибо, это правда помогает.", "en": "Premium is on until {date}. Thank you, it really helps."},
    "premium.failed": {"ru": "Оплата не прошла: {error}", "en": "Payment failed: {error}"},
    "premium.cancelled": {"ru": "Продление отменено. Premium работает до {date}.", "en": "Renewal cancelled. Premium works until {date}."},
    "premium.nothing": {"ru": "Активной подписки нет.", "en": "No active subscription."},
    "group.pro.paid": {"ru": "Pro для «{title}» включён до {date}.", "en": "Pro for “{title}” is on until {date}."},
    "pay.support": {
        "ru": "Вопросы по оплате: {contact}. Возврат делаем, если проверки не работали по нашей вине.",
        "en": "Payment questions: {contact}. We refund if checks didn't work because of us.",
    },

    "invite": {
        "ru": "<b>Позови друга</b>\n\nЗа каждого, кто придёт по ссылке, вам обоим +{bonus} проверок. Они не сгорают.\n\nУже пришли: {count}\n\n{link}",
        "en": "<b>Invite a friend</b>\n\nFor everyone who joins with your link, you both get +{bonus} checks that never expire.\n\nJoined so far: {count}\n\n{link}",
    },
    "invite.share": {"ru": "Проверяю файлы и ссылки на вирусы прямо в Telegram", "en": "I check files and links for malware right in Telegram"},

    "history.title": {"ru": "<b>Последние проверки</b>", "en": "<b>Recent checks</b>"},
    "history.empty": {"ru": "Проверок пока нет. Пришли файл, начнём.", "en": "No checks yet. Send a file to start."},

    "help": {
        "ru": (
            "<b>Как пользоваться</b>\n\n"
            "<b>В личке.</b> Пришли файл, ссылку или хэш. Знакомые файлы проверяются мгновенно, новые до пары минут.\n\n"
            "<b>В чате.</b> Добавь меня и дай право удалять сообщения. Я смотрю каждый файл и ссылку, опасное убираю. "
            "Настройки чата: /settings прямо в чате.\n\n"
            "<b>В канале.</b> Добавь меня в группу обсуждений канала. Файлы из постов я проверю и отвечу в комментариях.\n\n"
            "<b>В любом чате.</b> Напиши <code>@{bot} хэш или ссылка</code>, и результат можно отправить собеседнику.\n\n"
            "/history история · /settings настройки · /premium · /invite · /privacy · /support"
        ),
        "en": (
            "<b>How to use</b>\n\n"
            "<b>In private.</b> Send a file, a link or a hash. Known files are instant, new ones take up to a couple of minutes.\n\n"
            "<b>In groups.</b> Add me and allow deleting messages. I check every file and link and remove the dangerous ones. "
            "Group settings: /settings right in the group.\n\n"
            "<b>In channels.</b> Add me to the channel's discussion group. I'll check files from posts and answer in the comments.\n\n"
            "<b>Anywhere.</b> Type <code>@{bot} hash or link</code> and send the result to whoever you're talking to.\n\n"
            "/history · /settings · /premium · /invite · /privacy · /support"
        ),
    },
    "privacy": {
        "ru": (
            "<b>Что я храню</b>\n\n"
            "· отпечатки файлов и результаты проверок, они общие для всех\n"
            "· твою историю: имена файлов в зашифрованном виде\n"
            "· сами файлы не храню, удаляю сразу после проверки\n\n"
            "Новые файлы уходят в VirusTotal, если загрузка включена в /settings.\n\n"
            "/mydata выгрузить всё · /deletedata удалить всё\n\n"
            "Условия использования: {terms}\nПравила: {aup}\nКонфиденциальность: {privacy}\nОплата и возвраты: {refunds}"
        ),
        "en": (
            "<b>What I store</b>\n\n"
            "· file fingerprints and check results, shared for everyone\n"
            "· your history, with file names encrypted\n"
            "· never the files themselves, they're deleted right after the check\n\n"
            "New files go to VirusTotal if uploading is on in /settings.\n\n"
            "/mydata export everything · /deletedata delete everything\n\n"
            "Terms: {terms}\nAcceptable use: {aup}\nPrivacy: {privacy}\nPayments and refunds: {refunds}"
        ),
    },
    "consent.ask": {
        "ru": (
            "<b>Перед первой проверкой</b>\n\n"
            "Я проверяю файлы и ссылки через антивирусные сервисы. Если файла нет ни в одной базе, он уходит в VirusTotal, "
            "где его видят исследователи безопасности. Это выключается в /settings. Проверка снижает риск, но не даёт гарантий.\n\n"
            "Нажимая кнопку, ты подтверждаешь, что тебе есть 16 лет, и принимаешь "
            "<a href=\"{terms}\">Условия</a>, <a href=\"{aup}\">Правила использования</a> и "
            "<a href=\"{privacy}\">Политику конфиденциальности</a>."
        ),
        "en": (
            "<b>Before the first check</b>\n\n"
            "I check files and links with antivirus services. If a file isn't in any database, it goes to VirusTotal, "
            "where security researchers can see it. You can turn this off in /settings. A scan lowers the risk but can't guarantee anything.\n\n"
            "By tapping the button you confirm you are 16 or older and accept the "
            "<a href=\"{terms}\">Terms</a>, <a href=\"{aup}\">Acceptable Use Policy</a> and "
            "<a href=\"{privacy}\">Privacy Policy</a>."
        ),
    },
    "consent.yes": {"ru": "Мне есть 16, принимаю", "en": "I'm 16 or older, I accept"},
    "consent.needed": {"ru": "Сначала открой бота и прими условия.", "en": "Open the bot and accept the terms first."},
    "google.advisory": {
        "ru": "Предупреждение от Google: {link}",
        "en": "Advisory provided by Google: {link}",
    },
    "delete.confirm": {
        "ru": "Удалить историю и настройки? Покупки и бонусы тоже пропадут. Отменить это нельзя.",
        "en": "Delete your history and settings? Purchases and bonuses go too. This can't be undone.",
    },
    "delete.yes": {"ru": "Удалить всё", "en": "Delete everything"},
    "delete.done": {"ru": "Удалил. Если вернёшься, начнём с чистого листа.", "en": "Deleted. If you come back, we start fresh."},
    "support.ask": {
        "ru": "Опиши, что случилось, одним сообщением. Я передам команде, ответ придёт сюда.",
        "en": "Describe what happened in one message. I'll pass it to the team and the reply comes here.",
    },
    "support.sent": {"ru": "Передал. Ответим здесь.", "en": "Sent. We'll reply here."},
    "support.reply": {"ru": "<b>Ответ поддержки</b>\n\n{text}", "en": "<b>Support reply</b>\n\n{text}"},

    "group.hello": {
        "ru": (
            "<b>Привет, я Чекни</b>\n\n"
            "Проверяю каждый файл и ссылку в этом чате. Опасное удалю, если дадите право удалять сообщения.\n\n"
            "Чистые файлы отмечаю реакцией, чтобы не засорять чат. Настройки: /settings"
        ),
        "en": (
            "<b>Hi, I'm Chekni</b>\n\n"
            "I check every file and link in this chat. I'll delete dangerous ones if you let me delete messages.\n\n"
            "Clean files just get a reaction so the chat stays tidy. Settings: /settings"
        ),
    },
    "group.need_admin": {
        "ru": "Чтобы удалять опасные файлы, мне нужно право удалять сообщения.",
        "en": "To remove dangerous files I need permission to delete messages.",
    },
    "group.settings": {
        "ru": "<b>Настройки чата «{title}»</b>\n\nПроверено: {scans}, угроз: {threats}.\nТариф: {plan}.",
        "en": "<b>Settings for “{title}”</b>\n\nChecked: {scans}, threats: {threats}.\nPlan: {plan}.",
    },
    "group.plan.free": {"ru": "бесплатный, до {limit} проверок в день", "en": "free, up to {limit} checks a day"},
    "group.plan.pro": {"ru": "Pro до {date}", "en": "Pro until {date}"},
    "group.loud": {"ru": "Отвечать на каждый файл", "en": "Reply to every file"},
    "group.delete_threats": {"ru": "Удалять опасное", "en": "Delete threats"},
    "group.scan_links": {"ru": "Проверять ссылки", "en": "Check links"},
    "group.share_unknown": {"ru": "Загружать новые файлы в VirusTotal", "en": "Upload new files to VirusTotal"},
    "group.clean_ttl": {"ru": "Убирать мои ответы о чистых файлах: {value}", "en": "Remove my clean-file replies: {value}"},
    "group.clean_ttl.never": {"ru": "никогда", "en": "never"},
    "group.clean_ttl.seconds": {"ru": "через {n} с", "en": "after {n}s"},
    "group.clean_ttl.minutes": {"ru": "через {n} мин", "en": "after {n} min"},
    "group.buy_pro": {"ru": "Pro для чата · {stars} ⭐", "en": "Pro for the chat · {stars} ⭐"},
    "group.admins_only": {"ru": "Настройки меняют только админы чата.", "en": "Only chat admins can change settings."},
    "group.limit": {
        "ru": "На сегодня бесплатные проверки в этом чате закончились. Админ может включить Pro: /settings",
        "en": "Free checks for this chat are used up today. An admin can turn on Pro: /settings",
    },
    "group.settings_in_private": {
        "ru": "Отправил настройки тебе в личку.",
        "en": "Sent the settings to you in private.",
    },
    "group.open_private": {
        "ru": "Напиши мне в личку, чтобы я мог прислать настройки: {link}",
        "en": "Message me in private so I can send the settings: {link}",
    },

    "chat.clean": {"ru": "🟢 <b>Чисто</b> · {name}\n{summary}", "en": "🟢 <b>Clean</b> · {name}\n{summary}"},
    "chat.clean.summary": {"ru": "0 из {total} антивирусов", "en": "0 of {total} engines"},
    "chat.suspicious": {
        "ru": "🟡 <b>Есть сомнения</b> · {name}\n{summary}\nОткрывайте, только если доверяете отправителю.",
        "en": "🟡 <b>Looks suspicious</b> · {name}\n{summary}\nOnly open it if you trust the sender.",
    },
    "chat.malicious": {
        "ru": "🔴 <b>Осторожно, опасный файл</b> · {name}\n{summary}\nНе открывайте его.",
        "en": "🔴 <b>Careful, dangerous file</b> · {name}\n{summary}\nDon't open it.",
    },
    "chat.url.malicious": {
        "ru": "🔴 <b>Опасная ссылка</b> · {host}\n{summary}\nНе переходите и не вводите там данные.",
        "en": "🔴 <b>Dangerous link</b> · {host}\n{summary}\nDon't open it or enter any details there.",
    },
    "chat.url.suspicious": {
        "ru": "🟡 <b>Подозрительная ссылка</b> · {host}\n{summary}",
        "en": "🟡 <b>Suspicious link</b> · {host}\n{summary}",
    },
    "chat.unknown": {
        "ru": "⚪️ <b>Проверить до конца не вышло</b> · {name}\nClamAV угроз не нашёл, но для точного ответа этого мало.",
        "en": "⚪️ <b>Couldn't finish the check</b> · {name}\nClamAV found nothing, but that's not enough for a verdict.",
    },
    "chat.hits": {"ru": "{hits} из {total} антивирусов: {threat}", "en": "{hits} of {total} engines: {threat}"},
    "chat.hits.plain": {"ru": "{hits} из {total} антивирусов нашли угрозу", "en": "{hits} of {total} engines found a threat"},
    "chat.signals": {"ru": "Файл маскируется под другой тип", "en": "The file disguises its real type"},
    "chat.deleted": {"ru": "Сообщение удалено.", "en": "Message removed."},
    "chat.too_big": {"ru": "⚪️ {name} больше 20 МБ, такие файлы Telegram мне не отдаёт.", "en": "⚪️ {name} is over 20 MB, Telegram won't let me download it."},
    "channel.post": {"ru": "Проверка файла из поста", "en": "Check of the file in this post"},

    "inline.prompt": {"ru": "Вставь хэш или ссылку", "en": "Paste a hash or a link"},
    "inline.prompt.desc": {"ru": "MD5, SHA-1, SHA-256 или https://…", "en": "MD5, SHA-1, SHA-256 or https://…"},
    "inline.unknown": {"ru": "Пока нет данных", "en": "No data yet"},
    "inline.unknown.desc": {"ru": "Нажми, чтобы отправить, проверка пойдёт в личке бота", "en": "Tap to send, the check will run in the bot chat"},
    "inline.unknown.text": {
        "ru": "Этого ещё нет в базах. Проверить можно тут: {link}",
        "en": "Not in the databases yet. You can check it here: {link}",
    },
    "guest.checking": {"ru": "Проверяю…", "en": "Checking…"},
    "guest.nothing": {
        "ru": "Ответь мной на сообщение с файлом или ссылкой, и я проверю.",
        "en": "Reply to a message with a file or a link and mention me, I'll check it.",
    },
}

PLURALS: dict[str, dict[str, tuple[str, ...]]] = {
    "check": {"ru": ("проверка", "проверки", "проверок"), "en": ("check", "checks")},
    "engine": {"ru": ("антивирус", "антивируса", "антивирусов"), "en": ("engine", "engines")},
    "file": {"ru": ("файл", "файла", "файлов"), "en": ("file", "files")},
}

UNITS = {"ru": ("Б", "КБ", "МБ", "ГБ"), "en": ("B", "KB", "MB", "GB")}


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


def size_label(lang: str, size: int) -> str:
    units = UNITS["en" if lang == "en" else "ru"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            text = f"{value:.0f}" if unit == units[0] or value >= 100 else f"{value:.1f}"
            if lang != "en":
                text = text.replace(".", ",")
            return f"{text} {unit}"
        value /= 1024
    return f"{size} {units[0]}"


def safe(text: str) -> str:
    return escape(text or "", quote=False)


def attr(text: str) -> str:
    return escape(text or "", quote=True)
