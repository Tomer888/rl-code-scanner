import requests
from bs4 import BeautifulSoup
from scanner.detector import extract_codes

SOURCES = [
    # Rocket League
    {"name": "rocket-league.com",        "url": "https://rocket-league.com/free-codes",                        "game": "Rocket League"},
    {"name": "pockettactics.com (RL)",    "url": "https://www.pockettactics.com/rocket-league/codes",           "game": "Rocket League"},
    {"name": "mrguider.org (RL)",         "url": "https://www.mrguider.org/roblox/rocket-league-codes/",        "game": "Rocket League"},
    # Fortnite
    {"name": "pockettactics.com (FN)",    "url": "https://www.pockettactics.com/fortnite/codes",                "game": "Fortnite"},
    {"name": "game8.co (FN)",             "url": "https://game8.co/games/Fortnite/archives/486504",             "game": "Fortnite"},
    {"name": "earlygame.com (FN)",        "url": "https://earlygame.com/codes/fortnite-codes",                  "game": "Fortnite"},
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; rl-code-scanner/1.0; +https://github.com/Tomer888/rl-code-scanner)"
}


def scrape_epicgames() -> dict:
    """
    Returns: {code: {"game": str, "description": str}}
    """
    all_codes = {}

    for source in SOURCES:
        try:
            resp = requests.get(source["url"], headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"[sites] Non-200 from {source['name']}: {resp.status_code}")
                continue

            soup = BeautifulSoup(resp.text, "lxml")
            text = soup.get_text(separator=" ")
            codes = extract_codes(text, "")
            for code, desc in codes.items():
                if code not in all_codes:
                    all_codes[code] = {"game": source["game"], "description": desc}
            print(f"[sites] {source['name']}: found {len(codes)} candidate code(s).")

        except requests.RequestException as e:
            print(f"[sites] Error fetching {source['name']}: {e}")

    print(f"[sites] Found {len(all_codes)} total candidate code(s) from tracking sites.")
    return all_codes
