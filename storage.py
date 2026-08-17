"""Local persistence for the Career Profile and the Quest Log.

Both live as plain files on disk so state survives across CLI sessions
without needing a database.
"""
import json
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
PROFILE_PATH = DATA_DIR / "career_profile.json"
QUEST_LOG_PATH = DATA_DIR / "quest_log.md"


def profile_exists() -> bool:
    return PROFILE_PATH.exists()


def load_profile() -> dict:
    if not profile_exists():
        return {}
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def save_profile(profile: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_PATH.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")


def profile_as_context(profile: dict) -> str:
    if not profile:
        return "(No Career Profile on file yet.)"
    lines = [f"- {key}: {value}" for key, value in profile.items()]
    return "\n".join(lines)


def append_quest_log_entry(markdown_entry: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    header = f"\n## {date.today().isoformat()}\n\n"
    with QUEST_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(header + markdown_entry.strip() + "\n")


def last_quest_log_entry() -> str:
    if not QUEST_LOG_PATH.exists():
        return "(No previous log entries yet.)"
    content = QUEST_LOG_PATH.read_text(encoding="utf-8")
    sections = content.split("\n## ")
    if not sections or not sections[-1].strip():
        return "(No previous log entries yet.)"
    return "## " + sections[-1].strip()
