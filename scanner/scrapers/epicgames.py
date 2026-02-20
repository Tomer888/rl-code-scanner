import requests
from scanner.detector import extract_codes

EPIC_FORUM_ENDPOINTS = [
    # Discourse JSON API: latest posts in the Rocket League category
    "https://community.epicgames.com/c/rocket-league/latest.json",
    # Search for recent code-related posts
    "https://community.epicgames.com/search.json?q=redeem+code+rocket+league&order=latest",
]

HEADERS = {
    "User-Agent": "rl-code-scanner/1.0 (github.com/YOUR_USERNAME/rl-code-scanner)",
    "Accept": "application/json",
}


def _scrape_html_fallback(html: str) -> set:
    """Fall back to BeautifulSoup plain-text extraction if JSON API is unavailable."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(separator=" ")
    return extract_codes(text, "")


def scrape_epicgames() -> set:
    all_codes = set()

    for endpoint in EPIC_FORUM_ENDPOINTS:
        try:
            resp = requests.get(endpoint, headers=HEADERS, timeout=15)

            if resp.status_code != 200:
                print(f"[epic] Non-200 from {endpoint}: {resp.status_code}")
                continue

            content_type = resp.headers.get("Content-Type", "")
            if "application/json" not in content_type:
                # HTML fallback
                all_codes.update(_scrape_html_fallback(resp.text))
                continue

            data = resp.json()

            # Discourse latest.json: topic list
            topics = data.get("topic_list", {}).get("topics", [])
            for topic in topics:
                title = topic.get("title", "")
                all_codes.update(extract_codes(title, ""))

            # Discourse search.json: full post content
            for post in data.get("posts", []):
                title = post.get("topic_title", "")
                body = post.get("cooked", "") + " " + post.get("raw", "")
                all_codes.update(extract_codes(title, body))

        except requests.RequestException as e:
            print(f"[epic] Error fetching {endpoint}: {e}")
        except (KeyError, ValueError) as e:
            print(f"[epic] Parse error for {endpoint}: {e}")

    print(f"[epic] Found {len(all_codes)} candidate code(s) from Epic Games forums.")
    return all_codes
