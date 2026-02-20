from scanner.scrapers.reddit import scrape_reddit
from scanner.scrapers.epicgames import scrape_epicgames
from scanner.state import load_seen_codes, save_seen_codes
from scanner.notifier import send_telegram_message


def main():
    print("[scan] Starting Rocket League code scan...")

    seen = load_seen_codes()
    print(f"[scan] {len(seen)} previously seen code(s) loaded from state.")

    found = set()
    found.update(scrape_reddit())
    found.update(scrape_epicgames())
    print(f"[scan] {len(found)} total candidate code(s) detected this run.")

    new_codes = found - seen

    if new_codes:
        print(f"[scan] NEW codes found: {new_codes}")
        send_telegram_message(new_codes)
    else:
        print("[scan] No new codes found this run.")

    save_seen_codes(seen | found)
    print("[scan] State saved. Done.")


if __name__ == "__main__":
    main()
