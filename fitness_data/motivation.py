"""
Motivational tips, quotes, and habit-building advice for Fitness Buddy.
"""
import random
from datetime import datetime

MOTIVATIONAL_QUOTES = [
    "💪 \"The only bad workout is the one that didn't happen.\"",
    "🌟 \"Take care of your body. It's the only place you have to live.\" — Jim Rohn",
    "🔥 \"It's not about being the best. It's about being better than you were yesterday.\"",
    "⚡ \"Your body can stand almost anything. It's your mind you have to convince.\"",
    "🏆 \"Success is the sum of small efforts, repeated day in and day out.\" — Robert Collier",
    "🌱 \"A year from now you'll wish you had started today.\" — Karen Lamb",
    "💫 \"Exercise is a celebration of what your body can do, not a punishment for what you ate.\"",
    "🎯 \"Don't limit your challenges — challenge your limits.\"",
    "🦋 \"Every rep, every set, every step brings you closer to the best version of yourself.\"",
    "🌊 \"Fitness is not about being better than someone else. It's about being better than you used to be.\"",
    "🚀 \"The hardest lift is lifting your butt off the couch.\"",
    "❤️ \"Love yourself enough to live a healthy lifestyle.\"",
    "🌻 \"Small steps every day add up to big changes.\"",
    "⭐ \"Your health is an investment, not an expense.\"",
    "🎖️ \"Sweat today, smile tomorrow.\"",
]

HABIT_TIPS = [
    "📅 **Habit Tip:** Set a specific workout time and treat it like a non-negotiable meeting with yourself.",
    "📝 **Habit Tip:** Track your workouts in a journal — seeing your progress is a powerful motivator.",
    "👥 **Habit Tip:** Find a workout buddy or share your goals with a friend for accountability.",
    "🎵 **Habit Tip:** Create an energizing playlist — music can boost workout performance by up to 15%.",
    "😴 **Habit Tip:** Prioritize 7–9 hours of sleep. Recovery happens while you rest!",
    "🧘 **Habit Tip:** Add 5 minutes of mindful breathing before and after your workout.",
    "🌅 **Habit Tip:** Lay out your workout clothes the night before to reduce morning friction.",
    "📸 **Habit Tip:** Take weekly progress photos — visual changes are often more motivating than the scale.",
    "🏃 **Habit Tip:** Start small. Even 10 minutes of movement daily builds a lasting habit.",
    "🎯 **Habit Tip:** Use the 2-minute rule — if a workout feels daunting, commit to just 2 minutes. You'll almost always continue.",
    "🍃 **Habit Tip:** Pair your workout with an existing habit (e.g., exercise right after your morning coffee).",
    "📊 **Habit Tip:** Set SMART goals: Specific, Measurable, Achievable, Relevant, and Time-bound.",
]

DAILY_CHALLENGES = [
    "🎯 **Today's Challenge:** Do 3 sets of 20 squats throughout the day — 1 set every 2 hours!",
    "🎯 **Today's Challenge:** Take a 10-minute brisk walk after each meal.",
    "🎯 **Today's Challenge:** Hold a plank for 30 seconds — 3 times today!",
    "🎯 **Today's Challenge:** Drink 8 glasses of water and track it.",
    "🎯 **Today's Challenge:** Do 10 push-ups every time you check your phone.",
    "🎯 **Today's Challenge:** Stretch for 5 minutes in the morning and 5 minutes before bed.",
    "🎯 **Today's Challenge:** Replace one processed snack with a fruit or handful of nuts.",
    "🎯 **Today's Challenge:** Go to bed 30 minutes earlier tonight for better recovery.",
    "🎯 **Today's Challenge:** Do 100 jumping jacks spread across the day.",
    "🎯 **Today's Challenge:** Write down 3 things you're grateful for your body achieving.",
]

WELLNESS_TIPS = [
    "🧘 **Wellness:** Practice deep breathing — 4 counts in, hold 4, out 4. Reduces cortisol and aids recovery.",
    "😴 **Wellness:** Poor sleep increases hunger hormones by 24%. Prioritize rest for better results.",
    "☀️ **Wellness:** Get 10–15 minutes of morning sunlight daily. It regulates your circadian rhythm.",
    "🧠 **Wellness:** Stress raises cortisol, which stores fat. Try 5 minutes of meditation today.",
    "🦵 **Wellness:** Active recovery (light walking, yoga) on rest days speeds up muscle repair.",
    "💊 **Wellness:** Magnesium-rich foods (nuts, leafy greens) improve sleep quality and muscle function.",
    "🌿 **Wellness:** Anti-inflammatory foods like berries, turmeric, and omega-3s reduce workout soreness.",
]


def get_daily_motivation() -> str:
    """Return a motivational message tailored to the day of the week."""
    day = datetime.now().strftime("%A")
    day_messages = {
        "Monday": "🌟 **Monday Reset!** A new week, a fresh start. Set your intentions and crush it!",
        "Tuesday": "🔥 **Tuesday Tune-Up!** Yesterday was just the warm-up. Keep that momentum going!",
        "Wednesday": "⚡ **Wednesday Warrior!** Halfway through the week — you're already winning!",
        "Thursday": "💪 **Thursday Thrive!** Almost there. Push hard today and coast into the weekend strong.",
        "Friday": "🏆 **Friday Finish Strong!** End the week with a great workout — you've earned it!",
        "Saturday": "🌈 **Saturday Fun!** Weekends are for active recovery and trying something new!",
        "Sunday": "🌿 **Sunday Recharge!** Rest, reflect, and prepare for another amazing week ahead.",
    }
    base_message = day_messages.get(day, "💫 Every day is a great day to move your body!")
    quote = random.choice(MOTIVATIONAL_QUOTES)
    habit = random.choice(HABIT_TIPS)
    challenge = random.choice(DAILY_CHALLENGES)

    return f"{base_message}\n\n{quote}\n\n{habit}\n\n{challenge}"


def get_random_motivation() -> str:
    """Return a random motivational quote."""
    return random.choice(MOTIVATIONAL_QUOTES)


def get_habit_tip() -> str:
    """Return a random habit-building tip."""
    return random.choice(HABIT_TIPS)


def get_wellness_tip() -> str:
    """Return a random wellness tip."""
    return random.choice(WELLNESS_TIPS)
