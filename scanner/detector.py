import re

# Pattern A: Hyphenated alphanumeric codes
# Rules to reduce false positives:
#   - Each segment must contain at least one letter (filters out pure-number dates like 2018-2020)
#   - Segments are 3-8 chars, uppercase letters + digits only
PATTERN_HYPHENATED = re.compile(
    r'\b((?=[A-Z0-9]*[A-Z][A-Z0-9]*)[A-Z0-9]{3,8}(?:-(?=[A-Z0-9]*[A-Z][A-Z0-9]*)[A-Z0-9]{3,8}){1,4})\b'
)

# Blocklist: patterns that look like codes but are always false positives
BLOCKLIST = re.compile(
    r'^\d{4}-\d{4}$'          # pure year ranges like 2018-2020
    r'|^\d{4}-\d{2}-\d{2}$'   # dates like 2024-01-15
    r'|^V\d+\.\d'              # version strings like V1.2
    r'|^[A-Z]{1,2}\d+$',      # short codes like S1, EP3
    re.IGNORECASE
)

# Pattern B: Known dictionary-style codes used in past Rocket League promotions
PATTERN_WORD_CODE = re.compile(
    r'\b(popcorn|bekind|couchpotato|rlbirthday|sarpbc|shazam|truffleshuffle|'
    r'rlnitro|season1|season2|season3|season4|season5|rlcs|rlwc|psyonix|'
    r'rlfree|titanium|goldengift|showboat|twinzer|breakout|octane|dominus)\b',
    re.IGNORECASE
)

# Context keywords: a code must appear near these to be considered a real promo code
# Covers both Rocket League and Fortnite
CONTEXT_KEYWORDS = re.compile(
    r'redeem|promo\s*code|free\s*code|code\s*drop|use\s*code|enter\s*code|'
    r'reward|decal|boost|antenna|topper|banner|title|cosmetic|rlcs|psyonix|'
    r'epic\s*games|in-?game|limited.time|exclusive|giveaway|'
    r'fortnite|v-?bucks|vbucks|skin|emote|pickaxe|glider|outfit|locker|'
    r'battle\s*pass|fnbr|chapter|season\s*\d',
    re.IGNORECASE
)

# Reward keywords to extract a short description near the code
REWARD_PATTERN = re.compile(
    r'([\w\s\-]{2,40}?)'
    r'\s*(?:skin|emote|decal|boost|banner|topper|antenna|wheels|'
    r'v-?bucks|vbucks|pickaxe|glider|outfit|wrap|spray|'
    r'cosmetic|item|reward|pack|bundle|dlc)',
    re.IGNORECASE
)

CONTEXT_WINDOW = 300  # Characters around a match to search for context keywords
DESCRIPTION_WINDOW = 150  # Smaller window to extract reward description


def has_context(text: str, match_start: int, match_end: int) -> bool:
    start = max(0, match_start - CONTEXT_WINDOW)
    end = min(len(text), match_end + CONTEXT_WINDOW)
    surrounding = text[start:end]
    return bool(CONTEXT_KEYWORDS.search(surrounding))


def extract_description(text: str, match_start: int, match_end: int) -> str:
    """Try to extract a short reward description near the code match."""
    start = max(0, match_start - DESCRIPTION_WINDOW)
    end = min(len(text), match_end + DESCRIPTION_WINDOW)
    surrounding = text[start:end]

    reward_match = REWARD_PATTERN.search(surrounding)
    if reward_match:
        desc = reward_match.group(0).strip()
        # Clean up whitespace and truncate
        desc = re.sub(r'\s+', ' ', desc)
        if len(desc) > 60:
            desc = desc[:60] + "..."
        return desc
    return ""


def extract_codes(title: str, body: str) -> dict:
    """
    Extract candidate promo codes from title and body text.
    Returns a dict: {code: description_or_empty_string}
    """
    combined = f"{title}\n{body}"
    found = {}

    for match in PATTERN_HYPHENATED.finditer(combined):
        code = match.group(1).upper()
        if BLOCKLIST.match(code):
            continue
        if has_context(combined, match.start(), match.end()):
            desc = extract_description(combined, match.start(), match.end())
            found[code] = found.get(code) or desc

    for match in PATTERN_WORD_CODE.finditer(combined):
        code = match.group(1).upper()
        desc = extract_description(combined, match.start(), match.end())
        found[code] = found.get(code) or desc

    return found
