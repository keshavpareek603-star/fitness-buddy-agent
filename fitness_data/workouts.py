"""
Workout recommendation data and logic for Fitness Buddy.
Provides structured workout plans based on user goals and fitness level.
"""

WORKOUTS = {
    "beginner": {
        "weight_loss": [
            {"name": "Jumping Jacks", "sets": 3, "reps": "30 sec", "rest": "15 sec"},
            {"name": "Bodyweight Squats", "sets": 3, "reps": 12, "rest": "30 sec"},
            {"name": "Wall Push-Ups", "sets": 3, "reps": 10, "rest": "30 sec"},
            {"name": "March in Place", "sets": 3, "reps": "1 min", "rest": "20 sec"},
            {"name": "Standing Bicycle Crunches", "sets": 2, "reps": 15, "rest": "30 sec"},
        ],
        "muscle_gain": [
            {"name": "Knee Push-Ups", "sets": 3, "reps": 10, "rest": "45 sec"},
            {"name": "Assisted Bodyweight Squats", "sets": 3, "reps": 12, "rest": "45 sec"},
            {"name": "Glute Bridges", "sets": 3, "reps": 15, "rest": "30 sec"},
            {"name": "Superman Hold", "sets": 3, "reps": "20 sec", "rest": "30 sec"},
            {"name": "Plank Hold", "sets": 3, "reps": "20 sec", "rest": "30 sec"},
        ],
        "flexibility": [
            {"name": "Cat-Cow Stretch", "sets": 2, "reps": "1 min", "rest": "15 sec"},
            {"name": "Child's Pose", "sets": 2, "reps": "1 min", "rest": "10 sec"},
            {"name": "Seated Forward Fold", "sets": 2, "reps": "45 sec", "rest": "15 sec"},
            {"name": "Hip Flexor Stretch", "sets": 2, "reps": "30 sec each", "rest": "15 sec"},
            {"name": "Chest Opener Stretch", "sets": 2, "reps": "30 sec", "rest": "10 sec"},
        ],
        "general_fitness": [
            {"name": "Brisk Walking (in place)", "sets": 1, "reps": "5 min", "rest": "1 min"},
            {"name": "Bodyweight Squats", "sets": 3, "reps": 10, "rest": "30 sec"},
            {"name": "Wall Push-Ups", "sets": 3, "reps": 8, "rest": "30 sec"},
            {"name": "Standing Side Crunches", "sets": 2, "reps": 12, "rest": "20 sec"},
            {"name": "Plank Hold", "sets": 2, "reps": "15 sec", "rest": "30 sec"},
        ],
    },
    "intermediate": {
        "weight_loss": [
            {"name": "Burpees", "sets": 4, "reps": 10, "rest": "30 sec"},
            {"name": "Jump Squats", "sets": 4, "reps": 12, "rest": "30 sec"},
            {"name": "Mountain Climbers", "sets": 3, "reps": "40 sec", "rest": "20 sec"},
            {"name": "High Knees", "sets": 3, "reps": "40 sec", "rest": "20 sec"},
            {"name": "Push-Ups", "sets": 3, "reps": 15, "rest": "30 sec"},
            {"name": "Bicycle Crunches", "sets": 3, "reps": 20, "rest": "20 sec"},
        ],
        "muscle_gain": [
            {"name": "Push-Ups", "sets": 4, "reps": 15, "rest": "45 sec"},
            {"name": "Bulgarian Split Squats", "sets": 3, "reps": 12, "rest": "45 sec"},
            {"name": "Pike Push-Ups", "sets": 3, "reps": 10, "rest": "45 sec"},
            {"name": "Reverse Lunges", "sets": 3, "reps": 12, "rest": "40 sec"},
            {"name": "Tricep Dips (chair)", "sets": 3, "reps": 12, "rest": "40 sec"},
            {"name": "Plank to Push-Up", "sets": 3, "reps": 8, "rest": "45 sec"},
        ],
        "flexibility": [
            {"name": "Sun Salutation Flow", "sets": 3, "reps": "1 round", "rest": "30 sec"},
            {"name": "Pigeon Pose", "sets": 2, "reps": "1 min each", "rest": "15 sec"},
            {"name": "Deep Lunge with Twist", "sets": 2, "reps": "45 sec each", "rest": "15 sec"},
            {"name": "Seated Spinal Twist", "sets": 2, "reps": "45 sec each", "rest": "10 sec"},
            {"name": "Standing Quad Stretch", "sets": 2, "reps": "45 sec each", "rest": "15 sec"},
        ],
        "general_fitness": [
            {"name": "Jump Rope (simulated)", "sets": 3, "reps": "1 min", "rest": "30 sec"},
            {"name": "Push-Ups", "sets": 3, "reps": 12, "rest": "30 sec"},
            {"name": "Bodyweight Lunges", "sets": 3, "reps": 12, "rest": "30 sec"},
            {"name": "Plank Hold", "sets": 3, "reps": "45 sec", "rest": "30 sec"},
            {"name": "Glute Bridges", "sets": 3, "reps": 15, "rest": "25 sec"},
        ],
    },
    "advanced": {
        "weight_loss": [
            {"name": "Burpee Box Jumps", "sets": 5, "reps": 10, "rest": "20 sec"},
            {"name": "Plyometric Push-Ups", "sets": 4, "reps": 12, "rest": "25 sec"},
            {"name": "Sprint Intervals (in place)", "sets": 6, "reps": "30 sec", "rest": "15 sec"},
            {"name": "Tuck Jumps", "sets": 4, "reps": 12, "rest": "20 sec"},
            {"name": "Mountain Climbers", "sets": 4, "reps": "50 sec", "rest": "15 sec"},
        ],
        "muscle_gain": [
            {"name": "Archer Push-Ups", "sets": 4, "reps": 10, "rest": "45 sec"},
            {"name": "Pistol Squat Progression", "sets": 4, "reps": 6, "rest": "60 sec"},
            {"name": "Diamond Push-Ups", "sets": 4, "reps": 12, "rest": "40 sec"},
            {"name": "Nordic Hamstring Curl", "sets": 3, "reps": 6, "rest": "60 sec"},
            {"name": "Handstand Hold", "sets": 3, "reps": "20 sec", "rest": "60 sec"},
            {"name": "L-Sit Hold", "sets": 3, "reps": "15 sec", "rest": "45 sec"},
        ],
        "flexibility": [
            {"name": "Full Yoga Flow (Vinyasa)", "sets": 1, "reps": "10 min", "rest": "—"},
            {"name": "Front Splits Progression", "sets": 3, "reps": "1 min each", "rest": "20 sec"},
            {"name": "Wheel Pose (Back Bridge)", "sets": 3, "reps": "30 sec", "rest": "30 sec"},
            {"name": "Standing Splits", "sets": 2, "reps": "45 sec each", "rest": "20 sec"},
        ],
        "general_fitness": [
            {"name": "Burpees", "sets": 5, "reps": 12, "rest": "20 sec"},
            {"name": "Plyometric Lunges", "sets": 4, "reps": 14, "rest": "25 sec"},
            {"name": "Push-Up Variations Circuit", "sets": 3, "reps": "1 min", "rest": "30 sec"},
            {"name": "V-Ups", "sets": 4, "reps": 15, "rest": "25 sec"},
            {"name": "Bear Crawl", "sets": 3, "reps": "30 sec", "rest": "20 sec"},
        ],
    },
}


def get_workout_plan(level: str, goal: str) -> list:
    """Return a workout plan for the given fitness level and goal."""
    level = level.lower().strip()
    goal = goal.lower().replace(" ", "_").strip()

    level_map = {"beginner": "beginner", "intermediate": "intermediate", "advanced": "advanced"}
    goal_map = {
        "weight_loss": "weight_loss",
        "lose_weight": "weight_loss",
        "muscle_gain": "muscle_gain",
        "build_muscle": "muscle_gain",
        "flexibility": "flexibility",
        "stretch": "flexibility",
        "general_fitness": "general_fitness",
        "general": "general_fitness",
        "stay_fit": "general_fitness",
    }

    resolved_level = level_map.get(level, "beginner")
    resolved_goal = goal_map.get(goal, "general_fitness")

    return WORKOUTS.get(resolved_level, WORKOUTS["beginner"]).get(
        resolved_goal, WORKOUTS["beginner"]["general_fitness"]
    )


def _parse_duration_seconds(value) -> float:
    """
    Convert a reps/duration value to seconds for duration estimation.
    Handles int (rep count, estimated 3 sec/rep), str like '30 sec', '1 min',
    '45 sec each', '1 round', or '—'.
    """
    import re
    if isinstance(value, int):
        return value * 3.0  # ~3 seconds per rep
    s = str(value).lower().strip()
    if s in ("—", "-", "1 round"):
        return 60.0  # rough estimate for flow exercises
    # e.g. "30 sec", "30 sec each", "1 min", "1 min each", "5 min", "10 min"
    m = re.match(r"(\d+(?:\.\d+)?)\s*(sec|min)", s)
    if m:
        num = float(m.group(1))
        unit = m.group(2)
        return num * 60 if unit == "min" else num
    # Plain number string
    try:
        return float(s) * 3.0
    except ValueError:
        return 30.0  # fallback


def _parse_rest_seconds(value) -> float:
    """Convert a rest value string to seconds."""
    import re
    s = str(value).lower().strip()
    if s in ("—", "-"):
        return 0.0
    m = re.match(r"(\d+(?:\.\d+)?)\s*(sec|min)", s)
    if m:
        num = float(m.group(1))
        unit = m.group(2)
        return num * 60 if unit == "min" else num
    try:
        return float(s)
    except ValueError:
        return 30.0


def calculate_workout_duration(plan: list) -> dict:
    """
    Estimate total workout duration for a plan (list of exercise dicts).

    Each exercise dict must have: sets (int), reps (int|str), rest (str).
    Adds 5 min warm-up and 5 min cool-down automatically.

    Returns:
        {
          "estimated_minutes": float,
          "valid": bool,
          "warning": str|None   (set if outside 10–90 min range)
        }
    """
    total_seconds = 0.0
    for ex in plan:
        sets = int(ex.get("sets", 1))
        reps_sec = _parse_duration_seconds(ex.get("reps", 10))
        rest_sec = _parse_rest_seconds(ex.get("rest", "30 sec"))
        total_seconds += sets * (reps_sec + rest_sec)

    # Add 5 min warm-up + 5 min cool-down
    total_seconds += 10 * 60

    minutes = round(total_seconds / 60, 1)
    warning = None
    if minutes < 10:
        warning = f"Plan is very short ({minutes} min). Consider adding more exercises."
    elif minutes > 90:
        warning = f"Plan may be too long ({minutes} min). Consider splitting into two sessions."

    return {
        "estimated_minutes": minutes,
        "valid": warning is None,
        "warning": warning,
    }


def format_workout_plan(level: str, goal: str) -> str:
    """Return a formatted, human-readable workout plan string."""
    plan = get_workout_plan(level, goal)
    display_goal = goal.replace("_", " ").title()
    display_level = level.title()

    duration_info = calculate_workout_duration(plan)

    lines = [
        f"🏋️ **{display_level} — {display_goal} Workout Plan**",
        "",
        "| # | Exercise | Sets | Reps/Duration | Rest |",
        "|---|----------|------|---------------|------|",
    ]
    for i, ex in enumerate(plan, 1):
        lines.append(f"| {i} | {ex['name']} | {ex['sets']} | {ex['reps']} | {ex['rest']} |")

    lines += [
        "",
        f"⏱️ *Estimated duration: ~{duration_info['estimated_minutes']} min (incl. 5 min warm-up & cool-down)*",
    ]
    if duration_info["warning"]:
        lines.append(f"⚠️ *{duration_info['warning']}*")
    lines.append("💡 *Warm up for 5 minutes before starting and cool down/stretch for 5 minutes after.*")
    return "\n".join(lines)
