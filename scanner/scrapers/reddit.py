import time
import requests
from scanner.detector import extract_codes

SUBREDDITS = [
    "RocketLeague",
    "RocketLeagueEsports",
]

HEADERS = {
    "User-Agent": "rl-code-scanner/1.0 (github.com/YOUR_USERNAME/rl-code-scanner)"
}

BASE_URL = "https://www.reddit.com/r/{subreddit}/new.json"
SEARCH_URL = "https://www.reddit.com/r/{subreddit}/search.json"


def fetch_new_posts(subreddit: str, limit: int = 100) -> list:
    url = BASE_URL.format(subreddit=subreddit)
    params = {"limit": limit, "sort": "new"}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()["data"]["children"]


def fetch_search_results(subreddit: str, query: str = "code redeem promo") -> list:
    url = SEARCH_URL.format(subreddit=subreddit)
    params = {
        "q": query,
        "sort": "new",
        "t": "week",
        "limit": 25,
        "restrict_sr": "true",
    }
    resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()["data"]["children"]


def scrape_reddit() -> set:
    all_codes = set()

    for subreddit in SUBREDDITS:
        try:
            posts = fetch_new_posts(subreddit)
            posts += fetch_search_results(subreddit)

            for child in posts:
                post = child["data"]
                title = post.get("title", "")
                body = post.get("selftext", "")
                all_codes.update(extract_codes(title, body))

            # Respect Reddit's ~10 req/min unauthenticated rate limit
            time.sleep(2)

        except requests.RequestException as e:
            print(f"[reddit] Error scraping r/{subreddit}: {e}")

    print(f"[reddit] Found {len(all_codes)} candidate code(s) across Reddit.")
    return all_codes
