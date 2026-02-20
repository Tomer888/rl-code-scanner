from scanner.scrapers.reddit import scrape_reddit
from scanner.scrapers.epicgames import scrape_epicgames
from scanner.state import load_seen_codes, save_seen_codes
from scanner.notifier import send_telegram_message


def main():
    print("[scan] Starting Rocket League + Fortnite code scan...")

    seen = load_seen_codes()
    print(f"[scan] {len(seen)} previously seen code(s) loaded from state.")

    # Scrape all sources — each returns {code: {"game": ..., "description": ...}}
    found = {}
    found.update(scrape_reddit())
    found.update(scrape_epicgames())
    print(f"[scan] {len(found)} total candidate code(s) detected this run.")

    # Only alert on codes we haven't seen before
    new_codes = {code: meta for code, meta in found.items() if code not in seen}

    if new_codes:
        print(f"[scan] NEW codes found: {list(new_codes.keys())}")
        send_telegram_message(new_codes)
    else:
        print("[scan] No new codes found this run.")

    # Save all seen codes (just the code strings, no metadata needed)
    save_seen_codes(seen | set(found.keys()))
    print("[scan] State saved. Done.")


if __name__ == "__main__":
    main()
