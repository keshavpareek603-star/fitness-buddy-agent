"""
Habit Tracker for Fitness Buddy.
Persists daily habit logs to data/habits.json.
"""
import json
import os
from datetime import datetime, timedelta

# ── Storage path ──────────────────────────────────────────────────────────────
_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
_HABITS_FILE = os.path.join(_DATA_DIR, "habits.json")


def _load() -> dict:
    """Load habits from JSON file. Returns empty dict on missing/corrupt file."""
    if not os.path.exists(_HABITS_FILE):
        return {}
    try:
        with open(_HABITS_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data: dict) -> None:
    """Persist habits dict to JSON file."""
    os.makedirs(_DATA_DIR, exist_ok=True)
    with open(_HABITS_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


# ── Public API ────────────────────────────────────────────────────────────────

def record_habit(habit_name: str, date_str: str) -> dict:
    """
    Record a completed habit for the given date.

    Args:
        habit_name: Name of the habit (e.g. "Morning Run").
        date_str:   ISO date string YYYY-MM-DD.

    Returns:
        {"success": True, "habit": habit_name, "date": date_str}
    """
    habit_name = habit_name.strip()
    data = _load()
    if date_str not in data:
        data[date_str] = []
    if habit_name not in data[date_str]:
        data[date_str].append(habit_name)
    _save(data)
    return {"success": True, "habit": habit_name, "date": date_str}


def get_habits(date_str: str) -> list:
    """Return list of habits completed on the given date."""
    data = _load()
    return data.get(date_str, [])


def get_all_habits() -> dict:
    """Return full habit history keyed by date."""
    return _load()


def get_weekly_summary(start_date_str: str) -> dict:
    """
    Return per-habit completion percentage over a 7-day window
    starting from start_date_str (inclusive).

    Returns:
        {
          "period": {"start": str, "end": str},
          "days_checked": int,
          "habits": {habit_name: {"days_completed": int, "percent": float}}
        }
    """
    try:
        start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}

    data = _load()
    dates = [(start + timedelta(days=i)).isoformat() for i in range(7)]

    # Collect all unique habit names seen in the window
    all_habits: set = set()
    for d in dates:
        all_habits.update(data.get(d, []))

    summary: dict = {}
    for habit in sorted(all_habits):
        days_done = sum(1 for d in dates if habit in data.get(d, []))
        summary[habit] = {
            "days_completed": days_done,
            "percent": round((days_done / 7) * 100, 1),
        }

    return {
        "period": {"start": dates[0], "end": dates[-1]},
        "days_checked": 7,
        "habits": summary,
    }
