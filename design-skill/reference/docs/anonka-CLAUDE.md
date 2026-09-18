# Анонка

Telegram-бот анонимных сообщений с мини-приложением. Человек берёт личную ссылку,
ставит её в био или сторис, ему пишут анонимно, он отвечает прямо в чате. Автора
не видно никому и никогда, это не продаётся.

## Где что

```
backend/app/
  bot/              aiogram: handlers/, keyboards, texts (ru+en), delivery, profile
  domain/           правила: users, inbox, filters, stats, analytics, billing, moderation, staff, privacy, broadcast, retention
  api/              FastAPI для мини-приложения: auth по initData, routes/ (me, inbox, admin)
  db/migrate.py     добавление колонок в существующие таблицы, новые колонки писать сюда
  story/render.py   карточка для сторис на Pillow
  db/models.py      все таблицы
  assets/           обложки для бота, арт для сторис, шрифты
frontend/src/       React 19 + Vite + Tailwind 4 + motion
  screens/          один файл на экран
  i18n/strings.ts   ru и en всегда вместе
docs/               DESIGN, VOICE, FEATURES, SECURITY, DEPLOY, brand/
```

Один процесс: polling бота и uvicorn в одном asyncio. Postgres и Redis в compose.

## Локально

```bash
cd backend && python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
cd ../frontend && npm install && npx tsc -b && npm run build
```

## Правила дома

- **Код без комментариев.** Имена должны объяснять сами.
- **Анонимность на уровне данных.** Telegram ID никогда не попадает в callback_data,
  ответы API, админские карточки и логи с текстом. Сообщения адресуются по `public_id`.
- **Никаких фейковых сообщений и платного раскрытия автора.** Это то, за что NGL
  заплатил $5M, и главная жалоба на конкурентов.
- **Тексты** по `docs/VOICE.md`: на «ты», без длинных тире, без восклицаний, эмодзи
  максимум одно и только по делу.
- **Дизайн** по `docs/DESIGN.md`: глянцевая глина на сплошном цвете, действия чернильные,
  без градиентов на поверхностях, без капслока.
- **Сборка фронта** минифицируется terser с `mangle.toplevel`, без sourcemap, без console.
- Коммиты прозой, `feat:` / `fix:` / `chore:`, без имени модели нигде.
