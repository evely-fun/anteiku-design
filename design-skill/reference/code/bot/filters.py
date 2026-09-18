import re

LOOKALIKES = str.maketrans({
    "a": "а", "e": "е", "o": "о", "p": "р", "c": "с", "x": "х", "y": "у", "k": "к", "m": "м",
    "t": "т", "b": "в", "h": "н", "3": "з", "0": "о", "6": "б", "@": "а", "ё": "е",
})

LINK = re.compile(
    r"(?:https?://|www\.|t\.me/|telegram\.me/|\b[a-z0-9-]{2,}\.(?:ru|com|me|org|net|io|su|рф|xyz|site|link|ly|gg|cc|to)\b)",
    re.IGNORECASE,
)

SEVERE = [re.compile(pattern) for pattern in (
    r"убе[йи]\s*себ", r"убейся", r"выпилис[ья]", r"вскрой(?:ся|сь)", r"повес(?:ься|ся)", r"сдохни",
    r"чтоб\s*ты\s*сдох", r"убью\s*тебя", r"тебя\s*убью", r"найду\s*тебя", r"знаю\s*где\s*ты\s*жив",
    r"прирежу", r"закопаю\s*тебя",
)] + [re.compile(pattern) for pattern in (r"\bkys\b", r"kill\s*your\s*self", r"i\s*will\s*kill\s*you")]

RUDE = [re.compile(pattern) for pattern in (
    r"\b(?:на|по|о|от|за|ни)?ху[йеияюё]", r"\bп[иеё]зд", r"\b(?:за|у|вы|от|до|на|по|раз|про|при)?[её]б(?:ан|ат|ал|ну|ыв|ись|ет|ут|ло|уч)",
    r"долбо[её]б", r"\bбля", r"\bсук[аиуе]?\b", r"\bмуд[аи]", r"\bшлюх", r"\bп[иe]д[оа]р", r"\bпедик",
    r"\bчмо\b", r"\bгандон", r"\bдебил", r"\bурод", r"\bмраз", r"\bтвар[ьи]", r"\bдаун\b",
)] + [re.compile(pattern) for pattern in (
    r"\bfuck", r"\bbitch", r"\bcunt", r"\bwhore", r"\bslut", r"\bfag", r"\bretard", r"\bnigg",
)]


def _normalize(text: str) -> str:
    lowered = text.lower()
    return re.sub(r"(.)\1{2,}", r"\1\1", lowered)


def _cyrillic(text: str) -> str:
    return text.translate(LOOKALIKES)


def has_link(text: str) -> bool:
    return bool(LINK.search(text))


def severity(text: str) -> str | None:
    if not text:
        return None
    plain = _normalize(text)
    variants = (plain, _cyrillic(plain))
    squeezed = re.sub(r"[^a-zа-я]", "", variants[1])
    for pattern in SEVERE:
        if any(pattern.search(variant) for variant in variants) or pattern.search(squeezed):
            return "severe"
    for pattern in RUDE:
        if any(pattern.search(variant) for variant in variants):
            return "rude"
    return None
