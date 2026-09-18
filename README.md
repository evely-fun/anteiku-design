# anteiku-design

Дизайн семьи Anteiku: Telegram-боты и мини-приложения Анонка, AnteikuAnon, AnteiCut и Чекни.

| папка | что внутри |
| --- | --- |
| [`design-skill/`](design-skill) | всё о стиле: визуальная система, глянцевая 3D-глина, UX бота и мини-приложения, голос и тексты, анти-слоп, инженерия, чек-листы, оригинальные документы проектов, эталонный код, скриншоты и арт. Начинать с [`design-skill/README.md`](design-skill/README.md). Оформлено как навык Claude (`SKILL.md`). |
| [`asset-gallery/`](asset-gallery) | все сгенерированные ассеты: 486 файлов в 39 папках, иконки, карточки, обложки игр, роли мафии, карты Бункера, портреты, рамки, фоны, анимация сундука, видео, бренды, исходники. В каждой папке README с превью. |

Для ИИ: если тебя попросили сделать что-то для этих проектов, сначала прочитай `design-skill/README.md`
целиком и выполни все шаги оттуда, включая собственный поиск в интернете.

## Как подключить навык в Claude Code

```bash
git clone https://github.com/evely-fun/anteiku-design.git
mkdir -p ~/.claude/skills && ln -s "$PWD/anteiku-design/design-skill" ~/.claude/skills/anteiku-design
```
