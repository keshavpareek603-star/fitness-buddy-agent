"""
Fitness Buddy — Flask Application Entry Point
IBM watsonx.ai (Granite) powered health & fitness coach.
"""
import os
from flask import Flask, request, jsonify, render_template_string, session
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv(override=True)

# ── Local modules ─────────────────────────────────────────────────────────────
from granite_ai import ask_granite, FALLBACK_RESPONSES, check_granite_connectivity, _credentials_configured
from fitness_data.workouts import format_workout_plan
from fitness_data.nutrition import format_meal_suggestion
from fitness_data.motivation import get_daily_motivation, get_wellness_tip
from fitness_data.habit_tracker import record_habit, get_habits
from fitness_data.progress import format_progress_report, get_weekly_progress

# ── Flask setup ───────────────────────────────────────────────────────────────
_secret = os.getenv("FLASK_SECRET_KEY", "")
if not _secret:
    raise RuntimeError(
        "FLASK_SECRET_KEY is not set. Add it to your .env file.\n"
        "Example: FLASK_SECRET_KEY=your-random-secret-string-here"
    )
app = Flask(__name__)
app.secret_key = _secret
CORS(app)

# ── HTML template (inline for single-file deployment) ────────────────────────
with open(os.path.join(os.path.dirname(__file__), "templates", "index.html"), "r", encoding="utf-8") as f:
    HTML_TEMPLATE = f.read()

# ── Validation constants ──────────────────────────────────────────────────────
_VALID_LEVELS = {"beginner", "intermediate", "advanced"}
_VALID_WORKOUT_GOALS = {"weight_loss", "lose_weight", "muscle_gain", "build_muscle",
                         "flexibility", "stretch", "general_fitness", "general", "stay_fit"}
_VALID_MEAL_GOALS = {"weight_loss", "lose_weight", "muscle_gain", "build_muscle",
                      "general_health", "general", "stay_healthy"}


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main chat UI."""
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Main conversational endpoint.
    Accepts: { "message": str, "history": list }
    Returns: { "response": str, "source": "granite"|"fallback" }
    """
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Store conversation in session
    if "history" not in session:
        session["history"] = []
    session["history"].append({"role": "user", "content": user_message})

    response_text = ask_granite(user_message, history)
    # Determine source: granite if credentials configured and no fallback marker
    using_fallback = (
        not _credentials_configured()
        or response_text in FALLBACK_RESPONSES.values()
    )
    source = "fallback" if using_fallback else "granite"

    session["history"].append({"role": "assistant", "content": response_text})
    # Keep session lean
    if len(session["history"]) > 20:
        session["history"] = session["history"][-20:]

    return jsonify({"response": response_text, "source": source})


@app.route("/api/workout", methods=["POST"])
def workout():
    """
    Quick workout plan endpoint.
    Accepts: { "level": str, "goal": str }
    Returns: { "plan": str }
    """
    data = request.get_json(silent=True) or {}
    level = data.get("level", "").strip().lower()
    goal = data.get("goal", "").strip().lower().replace(" ", "_")

    if not level:
        return jsonify({"error": "Missing required field: level"}), 400
    if level not in _VALID_LEVELS:
        return jsonify({
            "error": f"Invalid level '{level}'. Must be one of: {sorted(_VALID_LEVELS)}"
        }), 400
    if goal and goal not in _VALID_WORKOUT_GOALS:
        return jsonify({
            "error": f"Invalid goal '{goal}'. Must be one of: {sorted(_VALID_WORKOUT_GOALS)}"
        }), 400

    if not goal:
        goal = "general_fitness"

    plan = format_workout_plan(level, goal)
    return jsonify({"plan": plan})


@app.route("/api/meal", methods=["POST"])
def meal():
    """
    Meal suggestion endpoint.
    Accepts: { "goal": str, "diet": str (optional) }
    Returns: { "plan": str }
    """
    data = request.get_json(silent=True) or {}
    goal = data.get("goal", "").strip().lower().replace(" ", "_")
    diet = data.get("diet", "non-veg").strip()

    if not goal:
        return jsonify({"error": "Missing required field: goal"}), 400
    if goal not in _VALID_MEAL_GOALS:
        return jsonify({
            "error": f"Invalid goal '{goal}'. Must be one of: {sorted(_VALID_MEAL_GOALS)}"
        }), 400

    plan = format_meal_suggestion(goal, diet)
    return jsonify({"plan": plan})


@app.route("/api/motivate", methods=["GET"])
def motivate():
    """Return daily motivation message."""
    return jsonify({"message": get_daily_motivation()})


@app.route("/api/wellness", methods=["GET"])
def wellness():
    """Return a random wellness tip."""
    return jsonify({"tip": get_wellness_tip()})


@app.route("/api/habit", methods=["POST"])
def habit_record():
    """
    Record a completed habit.
    Accepts: { "habit": str, "date": str (YYYY-MM-DD) }
    Returns: { "success": bool, "habit": str, "date": str }
    """
    data = request.get_json(silent=True) or {}
    habit_name = data.get("habit", "").strip()
    date_str = data.get("date", "").strip()

    if not habit_name:
        return jsonify({"error": "Missing required field: habit"}), 400
    if not date_str:
        return jsonify({"error": "Missing required field: date"}), 400

    # Basic date format validation
    import re as _re
    if not _re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    result = record_habit(habit_name, date_str)
    return jsonify(result)


@app.route("/api/habits", methods=["GET"])
def habits_get():
    """
    Return habits for a given date.
    Query param: date=YYYY-MM-DD
    Returns: { "date": str, "habits": list }
    """
    date_str = request.args.get("date", "").strip()
    if not date_str:
        return jsonify({"error": "Missing query parameter: date"}), 400

    import re as _re
    if not _re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    habits = get_habits(date_str)
    return jsonify({"date": date_str, "habits": habits})


@app.route("/api/progress", methods=["GET"])
def progress_daily():
    """
    Return formatted progress report for a given date.
    Query param: date=YYYY-MM-DD
    Returns: { "date": str, "report": str }
    """
    date_str = request.args.get("date", "").strip()
    if not date_str:
        return jsonify({"error": "Missing query parameter: date"}), 400

    import re as _re
    if not _re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    report = format_progress_report(date_str)
    return jsonify({"date": date_str, "report": report})


@app.route("/api/progress/weekly", methods=["GET"])
def progress_weekly():
    """
    Return weekly progress summary.
    Query param: start=YYYY-MM-DD
    Returns: weekly summary dict from habit_tracker
    """
    start_str = request.args.get("start", "").strip()
    if not start_str:
        return jsonify({"error": "Missing query parameter: start"}), 400

    import re as _re
    if not _re.match(r"^\d{4}-\d{2}-\d{2}$", start_str):
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    summary = get_weekly_progress(start_str)
    return jsonify(summary)


@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    Pass ?probe=1 to perform a live IBM Granite connectivity test.
    Base call is instant (no network) — never exposes credentials.
    """
    configured = _credentials_configured()
    result = {
        "status": "ok",
        "service": "Fitness Buddy",
        "ibm_granite_configured": configured,
        "model": os.getenv("WATSONX_MODEL_ID", "ibm/granite-4-h-small"),
        "ibm_granite_connected": None,   # populated only on ?probe=1
        "granite_error": None,
    }
    if request.args.get("probe") == "1":
        granite = check_granite_connectivity()
        result["ibm_granite_connected"] = granite["connected"]
        result["granite_error"] = granite["error"]
    return jsonify(result)


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    print("=" * 60)
    print("  [*]  Fitness Buddy -- IBM Granite AI Health Coach")
    print("=" * 60)
    print(f"  ->  Running on http://localhost:{port}")
    if _credentials_configured():
        print("  [OK]  IBM watsonx.ai (Granite) -- credentials present")
    else:
        print("  [!]  IBM watsonx.ai -- NOT configured (using smart fallback)")
        print("       Add WATSONX_API_KEY & WATSONX_PROJECT_ID to .env")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=debug)
