# Чекни

Telegram-бот и мини-приложение для проверки файлов, ссылок, хэшей и QR-кодов на вирусы.
Работает в личке, охраняет группы и комментарии каналов, отвечает в inline-режиме и в guest mode
(в любом чате без добавления). Семья Anteiku: стиль как у Анонки и AnteiCut.

## Где что

```
backend/app/
  engines/          VirusTotal v3 (пул ключей, квота в Redis), abuse.ch, CIRCL, Web Risk, ClamAV
  scanning/         pipeline (сначала хэш, загрузка только неизвестного), inspect (магия байтов,
                    двойные расширения, RTLO, макросы, архивы), verdict (сведение), links, qr
  bot/              aiogram: handlers/, report (rich-карточка и запасной HTML), present, flows, texts
  domain/           users, quota, scans, chats, billing, staff, analytics, privacy, retention, broadcast
  api/              FastAPI для мини-приложения, контракт в docs/API.md
  db/models.py      все таблицы, новые колонки в db/migrate.py
frontend/src/       React 19 + Vite + Tailwind 4 + motion, один экран на файл
frontend/public/art verdict-*.jpg, картинка в шапке rich-отчёта
docs/               DESIGN, VOICE, SECURITY, FEATURES, DEPLOY, API, brand/
```

Один процесс: polling бота и uvicorn в одном asyncio. Postgres, Redis и ClamAV в compose.
Локальный Bot API сервер (файлы до 2 ГБ) включается профилем `bigfiles`.

## Локально

```bash
cd backend && python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
cd ../frontend && npm install && npx tsc -b && npm run build
```

## Правила дома

- **Код без комментариев.** Имена объясняют сами.
- **Файлы никогда не запускаются.** Только чтение байтов: хэш, сигнатуры, список архива без распаковки.
  Файл живёт в tmpfs `/scratch` с `noexec` и удаляется в `finally` сразу после проверки.
- **Сначала хэш.** Своя база, потом VirusTotal по хэшу, потом abuse.ch и ClamAV, загрузка только
  если файл не знает никто. Картинки, видео и текст в VirusTotal не загружаются никогда.
- **Приватность.** Имена файлов и ссылки шифруются Fernet, Telegram ID не попадает в callback_data,
  ответы API и админку. Проверки адресуются по `public_id`.
- **Честность вердикта.** «Чисто» только если файл реально видели антивирусы или он в NSRL.
  Локальная проверка без VirusTotal даёт «проверить до конца не вышло», а не «чисто».
- **Тексты** по `docs/VOICE.md`. **Дизайн** по `docs/DESIGN.md`.
- **VirusTotal Public API нельзя использовать коммерчески.** Перед монетизацией нужен Premium-ключ
  или другой движок, см. `docs/FEATURES.md`.
- Коммиты прозой, `feat:` / `fix:` / `chore:`, без имени модели нигде.
