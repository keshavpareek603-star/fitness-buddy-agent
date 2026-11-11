"""
tests/test_fitness_buddy.py
Comprehensive pytest test suite for Fitness Buddy.
Run: pytest tests/test_fitness_buddy.py -v
"""
import os
import sys
import json
import tempfile
import shutil
import pytest

# ── Make root importable from tests/ ─────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ── Patch data directory to a temp dir for all habit/progress tests ───────────
@pytest.fixture(autouse=True)
def _isolate_data_dir(tmp_path, monkeypatch):
    """Redirect habit_tracker data storage to a temp directory per test."""
    import fitness_data.habit_tracker as ht
    monkeypatch.setattr(ht, "_DATA_DIR", str(tmp_path))
    monkeypatch.setattr(ht, "_HABITS_FILE", str(tmp_path / "habits.json"))
    yield


# =============================================================================
# 1. Workout plan — levels
# =============================================================================

def test_workout_plan_levels():
    from fitness_data.workouts import get_workout_plan
    for level in ["beginner", "intermediate", "advanced"]:
        plan = get_workout_plan(level, "general_fitness")
        assert isinstance(plan, list), f"Expected list for level={level}"
        assert len(plan) > 0, f"Empty plan for level={level}"


# =============================================================================
# 2. Workout plan — goals
# =============================================================================

def test_workout_plan_goals():
    from fitness_data.workouts import get_workout_plan
    for goal in ["weight_loss", "muscle_gain", "flexibility", "general_fitness"]:
        plan = get_workout_plan("beginner", goal)
        assert isinstance(plan, list)
        assert len(plan) > 0, f"Empty plan for goal={goal}"
        assert "name" in plan[0]
        assert "sets" in plan[0]


# =============================================================================
# 3. Workout — invalid input falls back gracefully
# =============================================================================

def test_workout_invalid_input():
    from fitness_data.workouts import get_workout_plan
    plan = get_workout_plan("superhero", "flying")
    # Should fall back to a default plan, not crash
    assert isinstance(plan, list)
    assert len(plan) > 0


# =============================================================================
# 4. Workout duration — valid range
# =============================================================================

def test_workout_duration():
    from fitness_data.workouts import get_workout_plan, calculate_workout_duration
    for level in ["beginner", "intermediate", "advanced"]:
        for goal in ["weight_loss", "muscle_gain", "flexibility", "general_fitness"]:
            plan = get_workout_plan(level, goal)
            result = calculate_workout_duration(plan)
            mins = result["estimated_minutes"]
            assert 10 <= mins <= 90, (
                f"Duration {mins} min out of 10–90 range for {level}/{goal}"
            )


# =============================================================================
# 5. Meal plan — goals contain all meal times
# =============================================================================

def test_meal_plan_goals():
    from fitness_data.nutrition import get_meal_plan
    for goal in ["weight_loss", "muscle_gain", "general_health"]:
        plan = get_meal_plan(goal)
        for meal_time in ["breakfast", "lunch", "dinner", "snacks"]:
            assert meal_time in plan, f"Missing '{meal_time}' in plan for goal={goal}"
            assert len(plan[meal_time]) > 0


# =============================================================================
# 6. Meal dietary — vegetarian plan has no exclusively-non-veg items
# =============================================================================

def test_meal_dietary_veg():
    from fitness_data.nutrition import get_meal_plan
    for goal in ["weight_loss", "muscle_gain", "general_health"]:
        plan = get_meal_plan(goal, "vegetarian")
        for meal_time, items in plan.items():
            for item in items:
                diet_tags = item.get("diet", [])
                # An item is "exclusively non-veg" when non-veg is its only tag
                exclusively_non_veg = diet_tags == ["non-veg"]
                assert not exclusively_non_veg, (
                    f"Exclusively non-veg item '{item['name']}' found in vegetarian plan "
                    f"(goal={goal}, meal_time={meal_time})"
                )
                # Also must contain at least one veg-safe tag
                has_veg_safe = any(t in diet_tags for t in ("veg", "vegan", "eggetarian"))
                assert has_veg_safe, (
                    f"Item '{item['name']}' in vegetarian plan has no veg-safe tag "
                    f"(tags={diet_tags}, goal={goal}, meal_time={meal_time})"
                )


# =============================================================================
# 7. Meal dietary — vegan plan contains no animal products
# =============================================================================

def test_meal_dietary_vegan():
    from fitness_data.nutrition import get_meal_plan
    for goal in ["weight_loss", "muscle_gain", "general_health"]:
        plan = get_meal_plan(goal, "vegan")
        for meal_time, items in plan.items():
            for item in items:
                diet_tags = item.get("diet", [])
                # Must contain vegan or veg tag (no item should be non-veg/eggetarian only)
                has_vegan_safe = any(t in diet_tags for t in ("vegan", "veg"))
                assert has_vegan_safe, (
                    f"Item '{item['name']}' in vegan plan has no vegan/veg tag "
                    f"(tags={diet_tags}, goal={goal}, meal_time={meal_time})"
                )
                # No eggetarian-only items (egg-only tags without veg/vegan)
                egg_only = diet_tags == ["eggetarian"]
                assert not egg_only, (
                    f"Eggetarian-only item '{item['name']}' in vegan plan"
                )


# =============================================================================
# 8. Meal dietary — non-veg plan has at least one non-veg item
# =============================================================================

def test_meal_dietary_nonveg():
    from fitness_data.nutrition import get_meal_plan
    for goal in ["weight_loss", "muscle_gain", "general_health"]:
        plan = get_meal_plan(goal, "non-veg")
        all_items = [item for items in plan.values() for item in items]
        has_non_veg = any("non-veg" in item.get("diet", []) for item in all_items)
        assert has_non_veg, f"No non-veg items found in non-veg plan for goal={goal}"


# =============================================================================
# 9. Meal — format output contains disclaimer
# =============================================================================

def test_meal_calorie_disclaimer():
    from fitness_data.nutrition import format_meal_suggestion
    output = format_meal_suggestion("weight_loss")
    assert "Nutritional values are estimates only" in output, (
        "Disclaimer not found in format_meal_suggestion output"
    )


# =============================================================================
# 10. Meal — total calorie line is present in formatted output
# =============================================================================

def test_meal_calorie_totals():
    from fitness_data.nutrition import format_meal_suggestion
    output = format_meal_suggestion("muscle_gain")
    assert "Total Daily Calories" in output, (
        "Total calorie summary line missing from format_meal_suggestion output"
    )
    assert "kcal" in output


# =============================================================================
# 11. Motivation — not empty
# =============================================================================

def test_motivation_not_empty():
    from fitness_data.motivation import get_daily_motivation
    msg = get_daily_motivation()
    assert isinstance(msg, str)
    assert len(msg) > 20


# =============================================================================
# 12. Wellness tip — not empty
# =============================================================================

def test_wellness_tip_not_empty():
    from fitness_data.motivation import get_wellness_tip
    tip = get_wellness_tip()
    assert isinstance(tip, str)
    assert len(tip) > 10


# =============================================================================
# 13. Habit tracker — record and retrieve
# =============================================================================

def test_habit_record_and_retrieve():
    from fitness_data.habit_tracker import record_habit, get_habits
    result = record_habit("Morning Run", "2024-01-15")
    assert result["success"] is True
    habits = get_habits("2024-01-15")
    assert "Morning Run" in habits


# =============================================================================
# 14. Habit tracker — weekly summary returns dict with % values
# =============================================================================

def test_habit_weekly_summary():
    from fitness_data.habit_tracker import record_habit, get_weekly_summary
    record_habit("Meditation", "2024-01-15")
    record_habit("Meditation", "2024-01-16")
    record_habit("Hydration", "2024-01-15")
    summary = get_weekly_summary("2024-01-15")
    assert "habits" in summary
    assert "period" in summary
    assert "days_checked" in summary
    assert summary["days_checked"] == 7
    assert "Meditation" in summary["habits"]
    med = summary["habits"]["Meditation"]
    assert "percent" in med
    assert isinstance(med["percent"], float)
    assert 0.0 <= med["percent"] <= 100.0


# =============================================================================
# 15. Progress — empty data returns safe string, no crash
# =============================================================================

def test_progress_empty():
    from fitness_data.progress import format_progress_report
    # No habits recorded — should not crash
    report = format_progress_report("2024-01-01")
    assert isinstance(report, str)
    assert len(report) > 0
    # Should mention no habits tracked
    assert "No habits" in report or "not" in report.lower() or "yet" in report.lower()


# =============================================================================
# 16. Progress — with habits recorded shows data
# =============================================================================

def test_progress_with_habits():
    from fitness_data.habit_tracker import record_habit
    from fitness_data.progress import format_progress_report
    record_habit("Evening Walk", "2024-03-10")
    record_habit("Drink Water", "2024-03-10")
    report = format_progress_report("2024-03-10")
    assert isinstance(report, str)
    assert "Evening Walk" in report or "2" in report  # habits appear or count shows


# =============================================================================
# 17. Granite — ask with empty credentials returns fallback string
# =============================================================================

def test_granite_fallback(monkeypatch):
    # Credentials are read dynamically via _get_credentials() → os.getenv().
    # Use monkeypatch.setenv / delenv to control what os.getenv returns.
    monkeypatch.setenv("WATSONX_API_KEY", "")
    monkeypatch.delenv("IBM_API_KEY", raising=False)
    monkeypatch.setenv("WATSONX_PROJECT_ID", "")
    import granite_ai
    result = granite_ai.ask_granite("Tell me a workout")
    assert isinstance(result, str)
    assert len(result) > 10


# =============================================================================
# 18. Granite — fallback message does not contain placeholder key
# =============================================================================

def test_granite_no_key_leak(monkeypatch):
    monkeypatch.setenv("WATSONX_API_KEY", "")
    monkeypatch.delenv("IBM_API_KEY", raising=False)
    monkeypatch.setenv("WATSONX_PROJECT_ID", "")
    import granite_ai
    result = granite_ai.ask_granite("workout")
    assert "your_ibm_api_key_here" not in result
    assert "your_watsonx_api_key_here" not in result


# =============================================================================
# 19. Credentials configured — False when key is placeholder
# =============================================================================

def test_credentials_configured_false(monkeypatch):
    monkeypatch.setenv("WATSONX_API_KEY", "your_ibm_api_key_here")
    monkeypatch.delenv("IBM_API_KEY", raising=False)
    monkeypatch.setenv("WATSONX_PROJECT_ID", "some-project")
    import granite_ai
    assert granite_ai._credentials_configured() is False


# =============================================================================
# 20. Credentials configured — True with real-looking values
# =============================================================================

def test_credentials_configured_true(monkeypatch):
    monkeypatch.setenv("WATSONX_API_KEY", "real-api-key-abc123")
    monkeypatch.delenv("IBM_API_KEY", raising=False)
    monkeypatch.setenv("WATSONX_PROJECT_ID", "real-project-id-xyz")
    import granite_ai
    assert granite_ai._credentials_configured() is True


# =============================================================================
# Flask test client fixtures
# =============================================================================

@pytest.fixture
def flask_client():
    """Return a Flask test client with SECRET_KEY set."""
    os.environ.setdefault("FLASK_SECRET_KEY", "test-secret-key-for-pytest")
    import app as flask_app
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as client:
        yield client


# =============================================================================
# 21. Flask health endpoint
# =============================================================================

def test_flask_health(flask_client):
    resp = flask_client.get("/api/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"


# =============================================================================
# 22. Flask workout endpoint
# =============================================================================

def test_flask_workout_endpoint(flask_client):
    resp = flask_client.post(
        "/api/workout",
        json={"level": "beginner", "goal": "general_fitness"},
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "plan" in data
    assert len(data["plan"]) > 10


# =============================================================================
# 23. Flask meal endpoint
# =============================================================================

def test_flask_meal_endpoint(flask_client):
    resp = flask_client.post(
        "/api/meal",
        json={"goal": "general_health"},
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "plan" in data
    assert len(data["plan"]) > 10


# =============================================================================
# 24. Flask chat endpoint
# =============================================================================

def test_flask_chat_endpoint(flask_client):
    resp = flask_client.post(
        "/api/chat",
        json={"message": "Give me a workout tip"},
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "response" in data
    assert len(data["response"]) > 5
    assert data["source"] in ("granite", "fallback")


# =============================================================================
# 25. Flask habit endpoint — POST record + GET retrieve
# =============================================================================

def test_flask_habit_endpoint(flask_client):
    # Record
    resp = flask_client.post(
        "/api/habit",
        json={"habit": "Morning Yoga", "date": "2024-06-01"},
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True

    # Retrieve
    resp2 = flask_client.get("/api/habits?date=2024-06-01")
    assert resp2.status_code == 200
    data2 = resp2.get_json()
    assert "Morning Yoga" in data2["habits"]


# =============================================================================
# 26. Flask progress endpoint
# =============================================================================

def test_flask_progress_endpoint(flask_client):
    resp = flask_client.get("/api/progress?date=2024-06-01")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "report" in data
    assert isinstance(data["report"], str)


# =============================================================================
# 27. Flask input validation — bad level returns 400
# =============================================================================

def test_flask_input_validation(flask_client):
    resp = flask_client.post(
        "/api/workout",
        json={"level": "ultramaster", "goal": "general_fitness"},
        content_type="application/json",
    )
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data


# =============================================================================
# 28. Responsible AI disclaimer — medical query triggers disclaimer
# =============================================================================

def test_responsible_ai_disclaimer(monkeypatch):
    # Force fallback mode via env vars (credentials read dynamically)
    monkeypatch.setenv("WATSONX_API_KEY", "")
    monkeypatch.delenv("IBM_API_KEY", raising=False)
    monkeypatch.setenv("WATSONX_PROJECT_ID", "")
    import granite_ai
    response = granite_ai.ask_granite("I have a fever and chest pain symptoms")
    assert "Medical Disclaimer" in response or "medical" in response.lower(), (
        "Medical disclaimer not injected for medical query"
    )


# =============================================================================
# 29. IBM Granite live connectivity test (skipped if not configured)
# =============================================================================

def test_granite_live_connectivity():
    from granite_ai import check_granite_connectivity, _credentials_configured
    if not _credentials_configured():
        pytest.skip("IBM Granite credentials not configured — skipping live test")
    result = check_granite_connectivity()
    assert isinstance(result, dict), "check_granite_connectivity must return a dict"
    assert "connected" in result, "Result dict must have 'connected' key"
    assert isinstance(result["connected"], bool)
    assert "model" in result
    assert "error" in result
