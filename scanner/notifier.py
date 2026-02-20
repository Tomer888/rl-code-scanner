import os
import requests

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def send_telegram_message(codes: set) -> bool:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    code_list = "\n".join(f"  • `{code}`" for code in sorted(codes))
    message = (
        f"*Rocket League Promo Code{'s' if len(codes) > 1 else ''} Found!* 🎮\n\n"
        f"{len(codes)} new code{'s' if len(codes) > 1 else ''} detected:\n\n"
        f"{code_list}\n\n"
        f"Redeem in-game:\n"
        f"*Main Menu* → *Extras* → *Redeem Code*"
    )

    url = TELEGRAM_API.format(token=token)
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"[telegram] Notification sent for {len(codes)} new code(s).")
        return True
    except requests.RequestException as e:
        print(f"[telegram] Failed to send notification: {e}")
        return False
