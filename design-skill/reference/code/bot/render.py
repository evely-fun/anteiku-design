import io
import textwrap
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

from app.config import ASSETS

WIDTH, HEIGHT = 1080, 1920
THEMES = {
    "azure": ((26, 132, 247), (255, 255, 255)),
    "coral": ((255, 90, 78), (255, 255, 255)),
    "violet": ((139, 92, 246), (255, 255, 255)),
    "emerald": ((16, 185, 129), (255, 255, 255)),
    "amber": ((245, 165, 36), (38, 30, 20)),
    "ink": ((24, 26, 36), (255, 255, 255)),
}
CARD = (255, 251, 242)
CARD_INK = (34, 36, 48)
CARD_SOFT = (120, 118, 130)


@lru_cache
def _art() -> Image.Image:
    art = Image.open(ASSETS / "story" / "art.png").convert("RGBA")
    scale = WIDTH / art.width
    return art.resize((WIDTH, int(art.height * scale)), Image.LANCZOS)


@lru_cache
def _font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(ASSETS / "fonts" / f"Montserrat-{weight}.ttf"), size)


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    for columns in range(34, 8, -1):
        lines = textwrap.wrap(text, columns)
        if all(draw.textlength(line, font=font) <= width for line in lines):
            return lines
    return textwrap.wrap(text, 8)


def render(theme: str, headline: str, prompt: str, link: str, footer: str) -> bytes:
    background, ink = THEMES.get(theme, THEMES["azure"])
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), background + (255,))
    art = _art()
    canvas.alpha_composite(art, (0, 150))

    draw = ImageDraw.Draw(canvas)
    margin = 90
    card_top = 150 + art.height + 40
    title_font = _font("ExtraBold", 84)
    prompt_font = _font("Bold", 54)
    link_font = _font("SemiBold", 40)
    footer_font = _font("SemiBold", 34)

    title_lines = _wrap(draw, headline, title_font, WIDTH - margin * 2)
    y = card_top
    for line in title_lines[:3]:
        draw.text((margin, y), line, font=title_font, fill=ink)
        y += 100
    y += 40

    body = prompt or ""
    prompt_lines = _wrap(draw, body, prompt_font, WIDTH - margin * 2 - 100)[:5] if body else []
    card_height = 120 + len(prompt_lines) * 70 + (0 if prompt_lines else -40) + 90
    card_box = (margin, y, WIDTH - margin, y + card_height)
    draw.rounded_rectangle(card_box, radius=56, fill=CARD)
    inner = y + 60
    for line in prompt_lines:
        draw.text((margin + 50, inner), line, font=prompt_font, fill=CARD_INK)
        inner += 70
    if prompt_lines:
        inner += 20
    draw.text((margin + 50, inner), link, font=link_font, fill=CARD_SOFT)

    footer_width = draw.textlength(footer, font=footer_font)
    draw.text(((WIDTH - footer_width) / 2, HEIGHT - 170), footer, font=footer_font, fill=ink)

    buffer = io.BytesIO()
    canvas.convert("RGB").save(buffer, format="JPEG", quality=90, optimize=True)
    return buffer.getvalue()
