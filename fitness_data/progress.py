"""
Progress Dashboard for Fitness Buddy.
Provides daily and weekly progress reports derived from habit_tracker data.
"""
from datetime import datetime, timedelta
from fitness_data.habit_tracker import get_habits, get_weekly_summary, get_all_habits


def get_daily_progress(date_str: str) -> dict:
    """
    Return habits completed on the given date vs total habits ever tracked.

    Returns:
        {
          "date": str,
          "completed": int,
          "total_tracked": int,
          "habits": list[str],
          "percent": float,
        }
    """
    completed_habits = get_habits(date_str)
    all_data = get_all_habits()

    # Total unique habits ever tracked
    all_habit_names: set = set()
    for habits in all_data.values():
        all_habit_names.update(habits)

    total = len(all_habit_names) if all_habit_names else 0
    done = len(completed_habits)
    percent = round((done / total) * 100, 1) if total > 0 else 0.0

    return {
        "date": date_str,
        "completed": done,
        "total_tracked": total,
        "habits": completed_habits,
        "percent": percent,
    }


def get_weekly_progress(start_date_str: str) -> dict:
    """
    Return per-habit completion percentages over a 7-day window.
    Delegates to habit_tracker.get_weekly_summary.
    """
    return get_weekly_summary(start_date_str)


def format_progress_report(date_str: str) -> str:
    """
    Return a human-readable markdown progress report for the given date.
    Safe on empty data.
    """
    daily = get_daily_progress(date_str)

    if daily["total_tracked"] == 0:
        return (
            f"📊 **Progress Report — {date_str}**\n\n"
            "No habits are being tracked yet. "
            "Start by logging a habit using the Habit Tracker! 💪"
        )

    lines = [
        f"📊 **Progress Report — {date_str}**",
        "",
        f"✅ Habits completed today: **{daily['completed']} / {daily['total_tracked']}** "
        f"({daily['percent']}%)",
        "",
    ]

    if daily["habits"]:
        lines.append("**Completed today:**")
        for h in daily["habits"]:
            lines.append(f"  • ✅ {h}")
    else:
        lines.append("*No habits logged for this date yet.*")

    # 7-day summary starting from 6 days before the requested date
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
        week_start = (target - timedelta(days=6)).isoformat()
        weekly = get_weekly_summary(week_start)
        if weekly.get("habits"):
            lines += [
                "",
                f"📅 **7-Day Summary** ({weekly['period']['start']} → {weekly['period']['end']})",
                "",
            ]
            for habit, stats in weekly["habits"].items():
                bar_filled = int(stats["percent"] / 10)
                bar = "█" * bar_filled + "░" * (10 - bar_filled)
                lines.append(
                    f"  • {habit}: [{bar}] {stats['percent']}% "
                    f"({stats['days_completed']}/7 days)"
                )
    except (ValueError, KeyError):
        pass  # Graceful — don't crash if weekly data unavailable

    lines += [
        "",
        "> 💡 *Keep going! Consistency is the key to lasting results.*",
    ]
    return "\n".join(lines)
