"""
Fitness Buddy — Streamlit UI
IBM watsonx.ai (Granite) powered health & fitness coach.
Run: streamlit run streamlit_app.py
"""

import re
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from granite_ai import ask_granite
from fitness_data.workouts import format_workout_plan
from fitness_data.nutrition import format_meal_suggestion
from fitness_data.motivation import get_daily_motivation, get_wellness_tip, get_habit_tip
from fitness_data.habit_tracker import record_habit
from fitness_data.progress import format_progress_report

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fitness Buddy — AI Health Coach",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Chat message styling */
.user-msg {
    background: #2563eb;
    color: white;
    padding: .65rem 1rem;
    border-radius: 14px 14px 4px 14px;
    margin: .4rem 0 .4rem 15%;
    font-size: .9rem;
    line-height: 1.6;
}
.bot-msg {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: .65rem 1rem;
    border-radius: 14px 14px 14px 4px;
    margin: .4rem 15% .4rem 0;
    font-size: .9rem;
    line-height: 1.6;
}
.chat-container {
    max-height: 420px;
    overflow-y: auto;
    padding: .5rem;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    background: #fff;
    margin-bottom: .75rem;
}
.ibm-badge {
    background: #0f62fe;
    color: white;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: .72rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Hi! I'm **Fitness Buddy**, your AI-powered health and fitness coach!\n\n"
                "I can help you with:\n"
                "🏋️ **Workout plans** tailored to your level & goals\n"
                "🥗 **Nutritious meal ideas** for your goals\n"
                "💪 **Daily motivation** and habit-building strategies\n"
                "🧘 **Wellness tips** — sleep, hydration & recovery\n\n"
                "Ask me anything or use the tools in the **sidebar**! 🚀"
            ),
        }
    ]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏋️ Fitness Buddy")
    st.markdown('<span class="ibm-badge">🔵 IBM Granite (watsonx.ai)</span>', unsafe_allow_html=True)
    st.divider()

    # ── Workout Planner ──────────────────────────────────────
    st.markdown("### 🏋️ Workout Planner")
    w_level = st.selectbox(
        "Fitness Level",
        ["Beginner", "Intermediate", "Advanced"],
        key="w_level",
    )
    w_goal = st.selectbox(
        "Goal",
        ["General Fitness", "Weight Loss", "Muscle Gain", "Flexibility"],
        key="w_goal",
    )
    if st.button("Generate Workout Plan 🏃", use_container_width=True):
        goal_key = w_goal.lower().replace(" ", "_")
        plan = format_workout_plan(w_level.lower(), goal_key)
        st.session_state.messages.append(
            {"role": "user", "content": f"Show me a {w_level} workout plan for {w_goal}"}
        )
        st.session_state.messages.append({"role": "assistant", "content": plan})
        st.rerun()

    st.divider()

    # ── Meal Planner ─────────────────────────────────────────
    st.markdown("### 🥗 Meal Planner")
    m_goal = st.selectbox(
        "Nutrition Goal",
        ["General Health", "Weight Loss", "Muscle Gain"],
        key="m_goal",
    )
    m_diet = st.selectbox(
        "Dietary Preference",
        ["Non-Veg", "Vegetarian", "Vegan", "Eggetarian"],
        key="m_diet",
    )
    if st.button("Get Meal Suggestions 🍽️", use_container_width=True):
        goal_key = m_goal.lower().replace(" ", "_")
        diet_key = m_diet.lower()
        plan = format_meal_suggestion(goal_key, diet_key)
        st.session_state.messages.append(
            {"role": "user", "content": f"Give me a {m_diet} meal plan for {m_goal}"}
        )
        st.session_state.messages.append({"role": "assistant", "content": plan})
        st.rerun()

    st.divider()

    # ── Habit Tracker ────────────────────────────────────────
    st.markdown("### 📅 Habit Tracker")
    import datetime as _dt
    habit_name_input = st.text_input(
        "Habit name",
        placeholder="e.g. Morning Run, 8 Glasses Water…",
        key="habit_name_input",
    )
    habit_date_input = st.date_input(
        "Date",
        value=_dt.date.today(),
        key="habit_date_input",
    )
    if st.button("Log Habit ✅", use_container_width=True):
        if habit_name_input.strip():
            date_str = habit_date_input.isoformat()
            result = record_habit(habit_name_input.strip(), date_str)
            msg = f"✅ Habit logged: **{result['habit']}** on {result['date']}"
            st.session_state.messages.append(
                {"role": "user", "content": f"Log habit: {habit_name_input.strip()} for {date_str}"}
            )
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.rerun()
        else:
            st.warning("Please enter a habit name.")

    st.divider()

    # ── My Progress ──────────────────────────────────────────
    st.markdown("### 📊 My Progress")
    progress_date_input = st.date_input(
        "Select date",
        value=_dt.date.today(),
        key="progress_date_input",
    )
    if st.button("View Progress 📈", use_container_width=True):
        date_str = progress_date_input.isoformat()
        report = format_progress_report(date_str)
        st.session_state.messages.append(
            {"role": "user", "content": f"Show my progress for {date_str}"}
        )
        st.session_state.messages.append({"role": "assistant", "content": report})
        st.rerun()

    st.divider()

    # ── Quick Actions ────────────────────────────────────────
    st.markdown("### ⚡ Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💪 Motivate", use_container_width=True):
            msg = get_daily_motivation()
            st.session_state.messages.append({"role": "user", "content": "Give me daily motivation! 💪"})
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.rerun()
    with col2:
        if st.button("🧘 Wellness", use_container_width=True):
            tip = get_wellness_tip()
            st.session_state.messages.append({"role": "user", "content": "Give me a wellness tip."})
            st.session_state.messages.append({"role": "assistant", "content": tip})
            st.rerun()
    if st.button("📅 Habit Tip", use_container_width=True):
        tip = get_habit_tip()
        st.session_state.messages.append({"role": "user", "content": "Give me a habit-building tip."})
        st.session_state.messages.append({"role": "assistant", "content": tip})
        st.rerun()

    st.divider()

    # ── Clear chat ───────────────────────────────────────────
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

    st.markdown(
        "<div style='text-align:center;font-size:.7rem;color:#94a3b8;margin-top:1rem'>"
        "Powered by IBM watsonx.ai<br>Granite-3-8B-Instruct</div>",
        unsafe_allow_html=True,
    )

# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("## 💬 Chat with Fitness Buddy")

# Render conversation
chat_html = '<div class="chat-container">'
for msg in st.session_state.messages:
    content_escaped = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
    content_escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", content_escaped)
    content_escaped = content_escaped.replace("\n", "<br>")
    if msg["role"] == "user":
        chat_html += f'<div class="user-msg">👤 {content_escaped}</div>'
    else:
        chat_html += f'<div class="bot-msg">🤖 {content_escaped}</div>'
chat_html += "</div>"

st.markdown(chat_html, unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
with st.form(key="chat_form", clear_on_submit=True):
    cols = st.columns([8, 1])
    with cols[0]:
        user_input = st.text_input(
            "Your message",
            placeholder="Ask me about workouts, meals, motivation, wellness…",
            label_visibility="collapsed",
        )
    with cols[1]:
        submitted = st.form_submit_button("Send ➤", use_container_width=True)

if submitted and user_input.strip():
    user_text = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": user_text})

    # Build history list for Granite
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]
    ]

    with st.spinner("Thinking…"):
        response = ask_granite(user_text, history[-10:])

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ── Quick prompt chips ────────────────────────────────────────────────────────
st.markdown("**Quick prompts:**")
chip_cols = st.columns(4)
chips = [
    ("🏋️ Home Workout", "I want to start working out at home. Can you help me?"),
    ("🥗 Healthy Eating", "What are some healthy meal ideas for better nutrition?"),
    ("💧 Hydration Tips", "What are the best tips for staying hydrated?"),
    ("😴 Better Sleep", "How can I improve my sleep for better recovery?"),
]
for i, (label, prompt) in enumerate(chips):
    with chip_cols[i]:
        if st.button(label, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Thinking…"):
                response = ask_granite(prompt, [])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center;font-size:.75rem;color:#94a3b8'>"
    "🏋️ Fitness Buddy &nbsp;·&nbsp; Powered by "
    "<a href='https://www.ibm.com/products/watsonx-ai' target='_blank'>IBM watsonx.ai (Granite)</a>"
    " &nbsp;·&nbsp; IBM Cloud Lite &nbsp;·&nbsp; 2024"
    "</div>",
    unsafe_allow_html=True,
)
