# 08. Инженерия

## Стек (одинаковый для Анонки, Чекни, AnteiCut)

- **Бэкенд**: Python 3.12, aiogram 3.31+, FastAPI, SQLAlchemy 2 async, Postgres 16 (asyncpg), Redis 7,
  Pillow для рендера картинок, cryptography (Fernet) для шифрования текстов и имён.
  Один процесс: polling бота и uvicorn в одном asyncio.
- **Фронт**: React 19, Vite 8, Tailwind 4 (`@tailwindcss/vite`), `motion`, Montserrat из fontsource, TypeScript 6, oxlint.
- **Сборка фронта обфусцирована** (`reference/code/frontend/vite.config.ts`): terser, `mangle.toplevel`,
  `drop_console`, без sourcemap, без комментариев, отдельные чанки vendor и motion.
- Фронт собирается в том же Dockerfile (node stage) и отдаётся FastAPI как статика.

## Структура проекта

```
<проект>/
  CLAUDE.md               правила дома и карта проекта
  backend/app/
    bot/                  handlers/, keyboards, texts (ru+en), covers, profile, middlewares
    domain/               бизнес-правила: users, inbox/scans, stats, analytics, billing, moderation, staff, privacy, retention, broadcast
    api/                  FastAPI для мини-приложения: auth по initData, deps, routes/
    db/models.py          все таблицы; db/migrate.py добавляет новые колонки в существующие таблицы
    assets/               обложки для бота, арт, шрифты
  backend/tests/          pytest: полный сценарий через диспетчер aiogram с фейковой сессией Telegram + API через httpx
  frontend/src/           app/, api/, i18n/, lib/, screens/ (один экран на файл), ui/ (kit, icons, marks), admin/
  frontend/public/legal/  условия, конфиденциальность, безопасность (ru + en)
  docs/                   DESIGN, VOICE, FEATURES, SECURITY, DEPLOY, LAUNCH, brand/, screens/
  deploy/                 nginx.conf, backup.sh, install-backup-cron.sh
  docker-compose.yml      app + postgres + redis
  deploy.sh
```

## Стиль кода

- **Без комментариев.** Имена объясняют сами.
- Код читается как окружающий: те же идиомы, та же плотность.
- Все строки UI в `i18n/strings.ts` сразу ru и en; все тексты бота в `bot/texts.py` сразу ru и en.
- Сервер решает, клиент рисует: роли, деньги, лимиты проверяются на бэкенде.
- Приватность на уровне данных: Telegram ID никогда не в `callback_data`, не в ответах API, не в админке.
  Сообщения и объекты адресуются по `public_id`.
- Коммиты прозой, `feat:` / `fix:` / `chore:`, без имени модели нигде.

## Хост

- Проекты лежат в `/home/deploy/<проект>`, каждый в docker compose на своём порту `127.0.0.1:80xx`.
- Перед ними системный nginx (`/etc/nginx/sites-enabled/<проект>`), TLS через certbot, домены вида
  `<проект>.40-160-90-130.sslip.io`, логи доступа для приватных продуктов выключены.
- Бэкапы Postgres в `/home/deploy/backups`, cron из `deploy/install-backup-cron.sh`.
- Git: `github.com/anteikucoder/telegram`, клон `/home/deploy/telegram`, у каждого проекта своя папка.

## Проверка

```bash
cd backend && .venv/bin/python -m pytest -q          # и на sqlite, и на Postgres (TEST_DATABASE_URL)
cd frontend && npx tsc -b && npx oxlint && npm run build
```

Визуально: Playwright (`~/.cache/ms-playwright/chromium-*`), фейковый `window.Telegram.WebApp` с подписанным
initData, скрипт telegram.org заглушить через `context.route`. Матрица: ru и en, светлая и тёмная, 360×640,
390×844, 430×932. Автопроверка горизонтального переполнения и ошибок консоли. Скриншот это доказательство,
слова нет.
