# 🏋️ Fitness Buddy — AI-Powered Health & Fitness Coach

> **IBM Cloud Lite / IBM watsonx.ai (Granite) powered conversational fitness assistant**

---

## 📋 Problem Statement

In today's fast-paced world, individuals struggle to maintain a healthy lifestyle due to lack of personalised guidance, time constraints, and inconsistent motivation. Fitness Buddy solves this with an accessible, AI-powered virtual coach available 24/7.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏋️ Workout Planner | Home workout plans for Beginner / Intermediate / Advanced levels |
| 🥗 Meal Suggestions | Personalised daily meal ideas with macros for Weight Loss, Muscle Gain, or General Health |
| 💪 Daily Motivation | Day-specific quotes, habit tips, and daily challenges |
| 🧘 Wellness Tips | Sleep, hydration, stress management, and recovery advice |
| 💬 AI Chat | Conversational interface powered by IBM Granite (ibm/granite-4-h-small) |
| 📅 Habit Building | Science-backed strategies for building consistent fitness routines |

---

## 🔵 IBM Technology Used

| Service | Details |
|---|---|
| **IBM watsonx.ai** | Granite LLM hosted on IBM Cloud (Lite plan eligible) |
| **Model** | `ibm/granite-4-h-small` |
| **SDK** | `ibm-watsonx-ai` Python SDK (≥ 1.9.1) |
| **Region** | `us-south` default (Frankfurt `eu-de` and others configurable) |

> **Lite Plan Eligibility:** IBM watsonx.ai offers a free Lite plan with monthly token allowances — no credit card required.  
> Sign up at: https://cloud.ibm.com

---

## 🚀 Quick Start

### 1. Clone / Download the project

```bash
cd fitness-buddy
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure IBM credentials

Copy `env.example` to `.env` and fill in your IBM credentials:

```bash
copy env.example .env   # Windows
cp env.example .env     # Mac/Linux
```

Edit `.env`:

```env
WATSONX_API_KEY=your_actual_ibm_api_key
WATSONX_PROJECT_ID=your_actual_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-4-h-small
FLASK_SECRET_KEY=your-long-random-secret-string
```

Generate a secure Flask secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run the app

```bash
python app.py
```

Open your browser at **http://localhost:5000**

**Or run with Streamlit (recommended):**
```bash
streamlit run streamlit_app.py
```
Open **http://localhost:8501**

---

## 🔑 Getting IBM Credentials (Free Lite Plan)

1. **Create IBM Cloud account:** https://cloud.ibm.com/registration
2. **Create API Key:**  
   IBM Cloud Console → Manage → IAM → API Keys → Create
3. **Create watsonx.ai Project:**  
   https://dataplatform.cloud.ibm.com → New Project → Copy the Project ID

---

## 📁 Project Structure

```
fitness-buddy/
│
├── streamlit_app.py          # Streamlit app (primary entry point)
├── app.py                    # Flask app (alternative entry point)
├── granite_ai.py             # IBM Granite / watsonx.ai integration
├── requirements.txt          # Python dependencies
├── .env                      # Your IBM credentials (do NOT commit)
├── env.example               # .env template (safe to commit)
│
├── fitness_data/
│   ├── __init__.py
│   ├── workouts.py           # Workout plans (Beginner/Intermediate/Advanced)
│   ├── nutrition.py          # Meal plans and macro guidance
│   └── motivation.py         # Quotes, habits, daily challenges
│
└── templates/
    └── index.html            # Flask chat UI frontend
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Chat UI |
| POST | `/api/chat` | AI chat (Granite) |
| POST | `/api/workout` | Get workout plan |
| POST | `/api/meal` | Get meal suggestions |
| GET | `/api/motivate` | Daily motivation |
| GET | `/api/wellness` | Wellness tip |
| GET | `/api/health` | Service health check |

### Example: Chat API

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Give me a beginner workout plan for weight loss"}'
```

### Example: Workout API

```bash
curl -X POST http://localhost:5000/api/workout \
  -H "Content-Type: application/json" \
  -d '{"level": "intermediate", "goal": "muscle_gain"}'
```

---

## 🤖 How IBM Granite AI Works

```
User Message
     │
     ▼
granite_ai.py
     │
     ├─── Credentials configured? ──YES──▶ IBM watsonx.ai API
     │                                          │
     │                                    Granite-3-8B
     │                                    (ibm/granite-4-h-small)
     │                                          │
     └─── NO ──────────────────────────▶ Smart Rule-Based Fallback
                                               │
                                         Keyword detection
                                         Pre-built responses
     │
     ▼
   Response → User
```

---

## 🛡️ Smart Fallback Mode

If IBM credentials are not configured, Fitness Buddy automatically switches to **Smart Fallback Mode** — a keyword-based response system that still provides:
- Workout guidance prompts
- Nutrition information
- Motivational quotes
- Wellness tips

This means the app works even without API credentials for demonstration purposes.

---

## 📦 Dependencies

| Package | Min Version | Purpose |
|---|---|---|
| streamlit | 1.40.0 | Streamlit UI (primary) |
| flask | 3.0.3 | Flask web framework (alternative) |
| flask-cors | 4.0.1 | CORS support |
| python-dotenv | 1.0.1 | Environment variables |
| ibm-watsonx-ai | 1.9.1 | IBM Granite SDK |
| requests | 2.32.3 | HTTP client |
| gunicorn | 22.0.0 | Production server |

---

## 🚀 Production Deployment

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

*Built for IBM Cloud Lite · Problem Statement #13 — Fitness Buddy*
