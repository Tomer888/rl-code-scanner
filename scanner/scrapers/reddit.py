import time
import xml.etree.ElementTree as ET
import requests
from scanner.detector import extract_codes

# Each subreddit tagged with its game
SUBREDDITS = [
    {"name": "RocketLeague",        "game": "Rocket League"},
    {"name": "RocketLeagueEsports", "game": "Rocket League"},
    {"name": "FortNiteBR",          "game": "Fortnite"},
    {"name": "FortniteCompetitive", "game": "Fortnite"},
]

RSS_URL = "https://www.reddit.com/r/{subreddit}/new/.rss"
SEARCH_RSS_URL = "https://www.reddit.com/r/{subreddit}/search/.rss?q=redeem+code+promo&restrict_sr=1&sort=new&t=week"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; rl-code-scanner/1.0; +https://github.com/Tomer888/rl-code-scanner)"
}

NS = {"atom": "http://www.w3.org/2005/Atom"}


def parse_rss(xml_text: str) -> list:
    entries = []
    try:
        root = ET.fromstring(xml_text)
        for entry in root.findall("atom:entry", NS):
            title_el = entry.find("atom:title", NS)
            content_el = entry.find("atom:content", NS)
            title = title_el.text or "" if title_el is not None else ""
            body = content_el.text or "" if content_el is not None else ""
            entries.append((title, body))
    except ET.ParseError as e:
        print(f"[reddit] RSS parse error: {e}")
    return entries


def scrape_reddit() -> dict:
    """
    Returns: {code: {"game": str, "description": str}}
    """
    all_codes = {}

    for sub in SUBREDDITS:
        subreddit = sub["name"]
        game = sub["game"]

        for url_template in [RSS_URL, SEARCH_RSS_URL]:
            url = url_template.format(subreddit=subreddit)
            try:
                resp = requests.get(url, headers=HEADERS, timeout=15)
                resp.raise_for_status()
                entries = parse_rss(resp.text)
                for title, body in entries:
                    codes = extract_codes(title, body)
                    for code, desc in codes.items():
                        if code not in all_codes:
                            all_codes[code] = {"game": game, "description": desc}
                print(f"[reddit] Fetched {len(entries)} entries from r/{subreddit}")
            except requests.RequestException as e:
                print(f"[reddit] Error fetching {url}: {e}")

            time.sleep(2)

    print(f"[reddit] Found {len(all_codes)} candidate code(s) across Reddit.")
    return all_codes
