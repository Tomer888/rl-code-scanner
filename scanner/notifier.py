import os
import requests
from collections import defaultdict

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"

GAME_EMOJI = {
    "Rocket League": "🚀",
    "Fortnite": "🎯",
}

REDEEM_INSTRUCTIONS = {
    "Rocket League": "Main Menu → Extras → Redeem Code",
    "Fortnite": "fortnite.com/redeem (login required)",
}


def send_telegram_message(new_codes: dict) -> bool:
    """
    new_codes: {code: {"game": str, "description": str}}
    """
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    # Group codes by game
    by_game = defaultdict(list)
    for code, meta in sorted(new_codes.items()):
        by_game[meta["game"]].append((code, meta.get("description", "")))

    lines = [f"*🎮 New Promo Codes Found! ({len(new_codes)} total)*\n"]

    for game, codes in by_game.items():
        emoji = GAME_EMOJI.get(game, "🎮")
        lines.append(f"{emoji} *{game}*")
        for code, desc in codes:
            line = f"  • `{code}`"
            if desc:
                line += f" — _{desc}_"
            lines.append(line)
        redeem = REDEEM_INSTRUCTIONS.get(game, "")
        if redeem:
            lines.append(f"  📍 Redeem: {redeem}")
        lines.append("")  # blank line between games

    message = "\n".join(lines).strip()

    url = TELEGRAM_API.format(token=token)
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"[telegram] Notification sent for {len(new_codes)} new code(s).")
        return True
    except requests.RequestException as e:
        print(f"[telegram] Failed to send notification: {e}")
        return False
