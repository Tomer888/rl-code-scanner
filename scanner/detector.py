import re

# Pattern A: Hyphenated alphanumeric codes (uppercase only to avoid URL/version false positives)
# Matches: AFA7-7522, ROCKET-XYZAB-12345, RLCS-ABC12-XYZ99
PATTERN_HYPHENATED = re.compile(
    r'\b([A-Z0-9]{3,8}(?:-[A-Z0-9]{3,8}){1,4})\b'
)

# Pattern B: Known dictionary-style codes used in past Rocket League promotions
PATTERN_WORD_CODE = re.compile(
    r'\b(popcorn|bekind|couchpotato|rlbirthday|sarpbc|shazam|truffleshuffle|'
    r'rlnitro|season1|season2|season3|season4|season5|rlcs|rlwc|psyonix|'
    r'rlfree|titanium|goldengift|showboat|twinzer|breakout|octane|dominus)\b',
    re.IGNORECASE
)

# Context keywords: a code must appear near these to be considered a real promo code
CONTEXT_KEYWORDS = re.compile(
    r'redeem|promo\s*code|free\s*code|code\s*drop|use\s*code|enter\s*code|'
    r'reward|decal|boost|antenna|topper|banner|title|cosmetic|rlcs|psyonix|'
    r'epic\s*games|in-?game|limited.time|exclusive|giveaway',
    re.IGNORECASE
)

CONTEXT_WINDOW = 300  # Characters around a match to search for context keywords


def has_context(text: str, match_start: int, match_end: int) -> bool:
    start = max(0, match_start - CONTEXT_WINDOW)
    end = min(len(text), match_end + CONTEXT_WINDOW)
    surrounding = text[start:end]
    return bool(CONTEXT_KEYWORDS.search(surrounding))


def extract_codes(title: str, body: str) -> set:
    combined = f"{title}\n{body}"
    found = set()

    for match in PATTERN_HYPHENATED.finditer(combined):
        code = match.group(1).upper()
        if has_context(combined, match.start(), match.end()):
            found.add(code)

    for match in PATTERN_WORD_CODE.finditer(combined):
        code = match.group(1).upper()
        # Word codes from the known list always count
        found.add(code)

    return found
