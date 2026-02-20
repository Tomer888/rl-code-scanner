import json
from pathlib import Path

STATE_FILE = Path("seen_codes.json")


def load_seen_codes() -> set:
    if STATE_FILE.exists():
        with STATE_FILE.open("r") as f:
            data = json.load(f)
        return set(data.get("codes", []))
    return set()


def save_seen_codes(codes: set) -> None:
    with STATE_FILE.open("w") as f:
        json.dump({"codes": sorted(codes)}, f, indent=2)
