import requests
from bs4 import BeautifulSoup
from scanner.detector import extract_codes

# Sites that track active Rocket League codes and update regularly
SOURCES = [
    {
        "name": "rocket-league.com",
        "url": "https://rocket-league.com/free-codes",
    },
    {
        "name": "pockettactics.com",
        "url": "https://www.pockettactics.com/rocket-league/codes",
    },
    {
        "name": "mrguider.org",
        "url": "https://www.mrguider.org/roblox/rocket-league-codes/",
    },
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; rl-code-scanner/1.0; +https://github.com/Tomer888/rl-code-scanner)"
}


def scrape_epicgames() -> set:
    """Scrape community code-tracking sites for active Rocket League codes."""
    all_codes = set()

    for source in SOURCES:
        try:
            resp = requests.get(source["url"], headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"[sites] Non-200 from {source['name']}: {resp.status_code}")
                continue

            soup = BeautifulSoup(resp.text, "lxml")
            text = soup.get_text(separator=" ")
            codes = extract_codes(text, "")
            all_codes.update(codes)
            print(f"[sites] {source['name']}: found {len(codes)} candidate code(s).")

        except requests.RequestException as e:
            print(f"[sites] Error fetching {source['name']}: {e}")

    print(f"[sites] Found {len(all_codes)} total candidate code(s) from tracking sites.")
    return all_codes
