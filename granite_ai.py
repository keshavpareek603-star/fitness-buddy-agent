"""
IBM Granite AI integration for Fitness Buddy.
Uses IBM watsonx.ai (ibm-watsonx-ai SDK) with the Granite model.

Environment variables (set in .env):
  WATSONX_API_KEY      — IBM Cloud IAM API key
  WATSONX_PROJECT_ID   — watsonx.ai project ID
  WATSONX_URL          — regional endpoint (default: eu-de Frankfurt)
  WATSONX_MODEL_ID     — Granite model ID (default: ibm/granite-4-h-small)

IMPORTANT: Credentials are read fresh from os.getenv() inside each function,
NOT at module level. This ensures load_dotenv(override=True) in the entry
point (app.py / streamlit_app.py) always wins regardless of import order.
"""
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# ── Placeholder guard ─────────────────────────────────────────────────────────
_PLACEHOLDER = {
    "your_ibm_api_key_here",
    "your_watsonx_api_key_here",
    "your_ibm_cloud_api_key_here",
    "",
}


# ── Credential accessors (always read fresh from env) ─────────────────────────

def _get_credentials() -> tuple:
    """
    Read credentials fresh from environment on every call.
    Supports WATSONX_API_KEY (preferred) and IBM_API_KEY (legacy).
    Returns: (api_key, url, project_id, model_id)
    """
    api_key    = os.getenv("WATSONX_API_KEY", "") or os.getenv("IBM_API_KEY", "")
    url        = os.getenv("WATSONX_URL",        "https://eu-de.ml.cloud.ibm.com")
    project_id = os.getenv("WATSONX_PROJECT_ID", "")
    model_id   = os.getenv("WATSONX_MODEL_ID",   "ibm/granite-4-h-small")
    return api_key, url, project_id, model_id


def _credentials_configured() -> bool:
    """Return True only when real (non-placeholder) credentials are present."""
    api_key, _, project_id, _ = _get_credentials()
    return api_key not in _PLACEHOLDER and project_id not in _PLACEHOLDER


# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Fitness Buddy, a friendly, knowledgeable, and encouraging AI-powered
health and fitness coach. You help users with:
- Personalized home workout recommendations
- Healthy meal and nutrition advice
- Motivational support and daily inspiration
- Habit-building strategies for a consistent fitness routine
- General wellness tips (sleep, hydration, stress management)

Guidelines:
- Always be positive, supportive, and non-judgmental
- Provide safe, evidence-based advice appropriate for home workouts
- Ask clarifying questions when needed (e.g., fitness level, goals, any injuries)
- Keep responses concise but comprehensive
- Add relevant emojis to make responses friendly and engaging
- Always recommend consulting a doctor before starting a new fitness program
- Never provide medical diagnoses or prescriptions

You are here to make fitness accessible, fun, and sustainable for everyone."""


# ── Model builder ─────────────────────────────────────────────────────────────

def _build_model():
    """
    Build and return an IBM watsonx.ai ModelInference client for IBM Granite.
    Returns None if credentials are missing/placeholder or SDK unavailable.

    Uses granite-4-h-small which is the chat-capable Granite model available
    on the Frankfurt (eu-de) watsonx.ai endpoint. Parameters are passed as
    native chat API params (max_tokens etc.) rather than GenTextParamsMetaNames
    which is not recognised by newer models.
    """
    if not _credentials_configured():
        return None

    api_key, url, project_id, model_id = _get_credentials()

    try:
        from ibm_watsonx_ai import APIClient, Credentials
        from ibm_watsonx_ai.foundation_models import ModelInference

        credentials = Credentials(url=url, api_key=api_key)
        client = APIClient(credentials)

        params = {
            "max_tokens": 800,
            "temperature": 0.7,
            "top_p": 0.9,
        }

        return ModelInference(
            model_id=model_id,
            api_client=client,
            project_id=project_id,
            params=params,
        )
    except ImportError:
        return None
    except Exception as exc:
        # Log to stderr for diagnostics — never expose raw credentials
        import sys as _sys
        api_key, _, project_id, _ = _get_credentials()
        err = str(exc)
        if api_key    and api_key    in err: err = err.replace(api_key,    "[REDACTED]")
        if project_id and project_id in err: err = err.replace(project_id, "[REDACTED]")
        print(f"[granite_ai] _build_model() failed: {type(exc).__name__}: {err}",
              file=_sys.stderr)
        return None


# ── Connectivity probe ────────────────────────────────────────────────────────

def check_granite_connectivity() -> dict:
    """
    Probe IBM Granite with a minimal request to verify real connectivity.
    Always returns a clean dict — no exceptions can escape.
    Returns: {"connected": bool, "model": str, "error": str|None}
    """
    try:
        _, _, _, model_id = _get_credentials()
        if not _credentials_configured():
            return {"connected": False, "model": model_id, "error": "Credentials not configured"}

        model = _build_model()
        if model is None:
            return {"connected": False, "model": model_id,
                    "error": "Failed to initialise IBM watsonx.ai client"}

        try:
            probe = model.chat(
                messages=[
                    {"role": "system", "content": "Reply with exactly one word: ready"},
                    {"role": "user",   "content": "ping"},
                ],
                params={"max_tokens": 10},
            )
            _ = probe  # any response = success
            return {"connected": True, "model": model_id, "error": None}

        except Exception as exc:
            api_key, _, project_id, _ = _get_credentials()
            msg = str(exc)
            if api_key    and api_key    in msg: msg = "Authentication or connectivity error (redacted)"
            if project_id and project_id in msg: msg = "Authentication or connectivity error (redacted)"
            return {"connected": False, "model": model_id, "error": msg}

    except Exception as outer:
        _, _, _, model_id = _get_credentials()
        return {"connected": False, "model": model_id,
                "error": f"Unexpected error: {type(outer).__name__}"}


# ── Responsible AI ────────────────────────────────────────────────────────────

_MEDICAL_KEYWORDS = [
    "diagnos", "symptom", "disease", "illness", "cancer", "diabetes",
    "heart attack", "stroke", "prescription", "medication", "dosage",
    "surgery", "chronic", "infection", "fever", "pain relief", "cure",
]

_MEDICAL_DISCLAIMER = (
    "⚠️ **Medical Disclaimer:** I am an AI fitness coach, not a medical professional. "
    "The information below is for general wellness purposes only and does not "
    "constitute medical advice, diagnosis, or treatment. "
    "Please consult a qualified healthcare provider for any medical concerns.\n\n"
    "---\n\n"
)


def _is_medical_query(message: str) -> bool:
    """Return True if the message appears to be asking about medical conditions."""
    return any(kw in message.lower() for kw in _MEDICAL_KEYWORDS)


# ── Primary AI function ───────────────────────────────────────────────────────

def ask_granite(user_message: str, conversation_history: list = None) -> str:
    """
    Send a message to IBM Granite and return the response.
    IBM Granite is always attempted first. Rule-based fallback is used only
    when credentials are absent or the API call fails.
    Prepends a responsible AI disclaimer for medical queries.

    Args:
        user_message:         The user's current message.
        conversation_history: List of {"role": "user"/"assistant", "content": str}.

    Returns:
        The assistant's response string.
    """
    medical = _is_medical_query(user_message)

    if not _credentials_configured():
        result = _fallback_response(user_message)
        return (_MEDICAL_DISCLAIMER + result) if medical else result

    model = _build_model()
    if model is None:
        return _fallback_response(user_message)

    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if conversation_history:
            messages.extend(conversation_history[-10:])
        messages.append({"role": "user", "content": user_message})

        response = model.chat(messages=messages)

        if isinstance(response, dict):
            choices = response.get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content", "").strip()
                if content:
                    return (_MEDICAL_DISCLAIMER + content) if medical else content

        raw = str(response).strip()
        return (_MEDICAL_DISCLAIMER + raw) if medical else raw

    except Exception as exc:
        api_key, _, project_id, _ = _get_credentials()
        err = str(exc)
        if api_key    and api_key    in err: err = "Authentication or connectivity error"
        if project_id and project_id in err: err = "Authentication or connectivity error"
        if "401" in err or "403" in err or "auth" in err.lower():
            fallback = (
                "⚠️ IBM watsonx.ai authentication failed. "
                "Please verify WATSONX_API_KEY and WATSONX_PROJECT_ID in your .env file.\n\n"
                + _fallback_response(user_message)
            )
            return (_MEDICAL_DISCLAIMER + fallback) if medical else fallback
        result = _fallback_response(user_message)
        return (_MEDICAL_DISCLAIMER + result) if medical else result


# ── Rule-based fallback ───────────────────────────────────────────────────────

FALLBACK_RESPONSES = {
    "workout": (
        "💪 I'd love to suggest a workout for you!\n\n"
        "Please tell me:\n"
        "1. Your fitness level (Beginner / Intermediate / Advanced)\n"
        "2. Your goal (Weight Loss / Muscle Gain / Flexibility / General Fitness)\n\n"
        "Or use the quick buttons to get an instant plan! 🏋️"
    ),
    "nutrition": (
        "🥗 Great choice focusing on nutrition!\n\n"
        "A balanced diet should include:\n"
        "• **Proteins:** Lean meats, legumes, eggs, dairy\n"
        "• **Carbs:** Whole grains, oats, sweet potatoes, fruits\n"
        "• **Healthy Fats:** Avocado, nuts, olive oil, salmon\n"
        "• **Veggies:** Aim for 5 servings of colorful vegetables daily\n\n"
        "Use the 🥗 Meal Plan button for personalized meal ideas!"
    ),
    "motivation": (
        "🌟 You've got this! Remember:\n\n"
        "\"The only bad workout is the one that didn't happen.\"\n\n"
        "Every step forward, no matter how small, is progress. "
        "Your future self will thank you for the effort you put in today! 💫\n\n"
        "Click 💪 Get Motivated for your daily dose of inspiration!"
    ),
    "sleep": (
        "😴 Sleep is your secret weapon!\n\n"
        "• Adults need **7–9 hours** of quality sleep\n"
        "• Sleep is when muscles repair and grow\n"
        "• Poor sleep increases hunger hormones by up to 24%\n"
        "• Tips: consistent bedtime, cool dark room, no screens 1hr before bed"
    ),
    "water": (
        "💧 Hydration is essential for fitness!\n\n"
        "• Aim for **8–10 glasses (2–2.5 litres)** daily\n"
        "• Drink 500ml **before** your workout\n"
        "• Sip water **during** exercise every 15–20 minutes\n"
        "• Rehydrate **after** with water or electrolyte drinks\n"
        "• Signs of dehydration: headache, dark urine, fatigue"
    ),
    "default": (
        "👋 Hi! I'm **Fitness Buddy**, your AI-powered health and fitness coach!\n\n"
        "I can help you with:\n"
        "🏋️ **Workout plans** tailored to your level and goals\n"
        "🥗 **Meal ideas** and nutrition guidance\n"
        "💪 **Daily motivation** and habit-building tips\n"
        "💧 **Wellness advice** on sleep, hydration, and recovery\n\n"
        "What would you like to work on today? Use the quick-action buttons or just ask me anything!"
    ),
}


def _fallback_response(message: str) -> str:
    """Return a rule-based response when IBM Granite is unavailable."""
    msg_lower = message.lower()
    if any(w in msg_lower for w in ["workout", "exercise", "train", "gym", "routine", "squat", "push"]):
        return FALLBACK_RESPONSES["workout"]
    if any(w in msg_lower for w in ["food", "eat", "meal", "diet", "nutrition", "calorie", "recipe"]):
        return FALLBACK_RESPONSES["nutrition"]
    if any(w in msg_lower for w in ["motivat", "inspire", "quote", "encourage", "tired", "lazy"]):
        return FALLBACK_RESPONSES["motivation"]
    if any(w in msg_lower for w in ["sleep", "rest", "recover", "insomnia"]):
        return FALLBACK_RESPONSES["sleep"]
    if any(w in msg_lower for w in ["water", "hydrat", "drink", "thirst"]):
        return FALLBACK_RESPONSES["water"]
    return FALLBACK_RESPONSES["default"]
