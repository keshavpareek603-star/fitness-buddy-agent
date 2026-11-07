"""
Nutrition and meal suggestion data for Fitness Buddy.
Provides meal ideas, macro guidance, and hydration tips.

Diet tags:
  vegan       — no animal products whatsoever
  veg         — vegetarian (dairy/eggs allowed, no meat/fish)
  eggetarian  — eggs allowed, no other meat/fish
  non-veg     — contains meat or fish
"""

MEAL_PLANS = {
    "weight_loss": {
        "breakfast": [
            {"name": "Greek Yogurt Parfait", "ingredients": "Low-fat Greek yogurt, mixed berries, 1 tbsp honey, granola", "calories": 320, "protein": "20g", "diet": ["veg"]},
            {"name": "Veggie Omelette", "ingredients": "3 egg whites, spinach, tomatoes, bell peppers, olive oil", "calories": 280, "protein": "22g", "diet": ["veg", "eggetarian"]},
            {"name": "Overnight Oats", "ingredients": "½ cup oats, almond milk, chia seeds, banana slices", "calories": 310, "protein": "12g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Smoothie Bowl", "ingredients": "Frozen berries, banana, spinach, almond milk, topped with seeds", "calories": 290, "protein": "10g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Tofu Scramble", "ingredients": "Firm tofu, turmeric, spinach, tomatoes, olive oil", "calories": 260, "protein": "18g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
        ],
        "lunch": [
            {"name": "Grilled Chicken Salad", "ingredients": "Chicken breast, mixed greens, cucumber, cherry tomatoes, lemon dressing", "calories": 380, "protein": "35g", "diet": ["non-veg"]},
            {"name": "Lentil Soup", "ingredients": "Red lentils, carrots, celery, cumin, turmeric, vegetable broth", "calories": 320, "protein": "18g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Tuna Lettuce Wraps", "ingredients": "Canned tuna, lettuce cups, avocado, red onion, lemon juice", "calories": 290, "protein": "28g", "diet": ["non-veg"]},
            {"name": "Quinoa Buddha Bowl", "ingredients": "Quinoa, roasted veggies, chickpeas, tahini drizzle", "calories": 420, "protein": "16g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Egg & Veggie Wrap", "ingredients": "Scrambled eggs, whole-wheat tortilla, spinach, salsa", "calories": 350, "protein": "20g", "diet": ["veg", "eggetarian"]},
        ],
        "dinner": [
            {"name": "Baked Salmon with Veggies", "ingredients": "Salmon fillet, broccoli, asparagus, garlic, olive oil", "calories": 420, "protein": "38g", "diet": ["non-veg"]},
            {"name": "Turkey Stir-Fry", "ingredients": "Ground turkey, mixed veggies, soy sauce, ginger, brown rice", "calories": 460, "protein": "32g", "diet": ["non-veg"]},
            {"name": "Cauliflower Rice Bowl", "ingredients": "Cauliflower rice, black beans, avocado, salsa, lime", "calories": 350, "protein": "14g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Grilled Chicken & Sweet Potato", "ingredients": "Chicken breast, sweet potato, steamed green beans", "calories": 440, "protein": "36g", "diet": ["non-veg"]},
            {"name": "Paneer Tikka with Salad", "ingredients": "Grilled paneer, mixed salad, yogurt dip, whole-wheat roti", "calories": 400, "protein": "22g", "diet": ["veg"]},
            {"name": "Dal & Brown Rice", "ingredients": "Yellow dal, brown rice, cucumber raita, roasted veggies", "calories": 380, "protein": "16g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
        ],
        "snacks": [
            {"name": "Apple with Almond Butter", "ingredients": "1 medium apple, 1 tbsp almond butter", "calories": 190, "protein": "4g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Celery & Hummus", "ingredients": "Celery sticks, 2 tbsp hummus", "calories": 80, "protein": "3g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Hard Boiled Eggs", "ingredients": "2 hard-boiled eggs, salt & pepper", "calories": 155, "protein": "13g", "diet": ["veg", "eggetarian"]},
            {"name": "Mixed Nuts (small handful)", "ingredients": "Almonds, walnuts, cashews (30g)", "calories": 180, "protein": "5g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
        ],
    },
    "muscle_gain": {
        "breakfast": [
            {"name": "Protein Pancakes", "ingredients": "Oats, banana, 2 eggs, protein powder, almond milk", "calories": 480, "protein": "35g", "diet": ["veg", "eggetarian"]},
            {"name": "Scrambled Eggs & Toast", "ingredients": "4 eggs, whole-grain toast, avocado, cheese", "calories": 520, "protein": "30g", "diet": ["veg", "eggetarian"]},
            {"name": "Oatmeal Power Bowl", "ingredients": "1 cup oats, protein powder, peanut butter, banana, milk", "calories": 600, "protein": "38g", "diet": ["veg", "eggetarian"]},
            {"name": "Vegan Protein Smoothie", "ingredients": "Plant protein powder, banana, almond milk, peanut butter, oats", "calories": 520, "protein": "32g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Chicken & Egg Breakfast Bowl", "ingredients": "Grilled chicken strips, 2 eggs, spinach, whole-grain toast", "calories": 560, "protein": "48g", "diet": ["non-veg"]},
        ],
        "lunch": [
            {"name": "Chicken & Rice Bowl", "ingredients": "200g chicken breast, brown rice, broccoli, teriyaki sauce", "calories": 580, "protein": "48g", "diet": ["non-veg"]},
            {"name": "Beef & Veggie Wrap", "ingredients": "Lean beef strips, whole-wheat tortilla, mixed veggies, hummus", "calories": 540, "protein": "38g", "diet": ["non-veg"]},
            {"name": "Salmon & Quinoa Plate", "ingredients": "Salmon, quinoa, mixed greens, olive oil dressing", "calories": 560, "protein": "42g", "diet": ["non-veg"]},
            {"name": "Paneer & Quinoa Bowl", "ingredients": "Grilled paneer, quinoa, roasted peppers, tahini dressing", "calories": 520, "protein": "30g", "diet": ["veg"]},
            {"name": "Tofu & Brown Rice Stir-Fry", "ingredients": "Firm tofu, brown rice, broccoli, soy sauce, sesame oil", "calories": 480, "protein": "26g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
        ],
        "dinner": [
            {"name": "Steak with Sweet Potato", "ingredients": "Lean steak, sweet potato, asparagus, olive oil", "calories": 620, "protein": "52g", "diet": ["non-veg"]},
            {"name": "Chicken Curry & Brown Rice", "ingredients": "Chicken thigh, coconut milk, spices, brown rice, peas", "calories": 580, "protein": "44g", "diet": ["non-veg"]},
            {"name": "Tuna Pasta", "ingredients": "Whole-wheat pasta, tuna, cherry tomatoes, spinach, olive oil", "calories": 560, "protein": "40g", "diet": ["non-veg"]},
            {"name": "Rajma & Rice (Kidney Bean Curry)", "ingredients": "Kidney beans, brown rice, onion-tomato masala, curd", "calories": 520, "protein": "22g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Egg Bhurji & Whole-Wheat Roti", "ingredients": "4 eggs, onion, tomato, spices, 2 whole-wheat rotis", "calories": 490, "protein": "30g", "diet": ["veg", "eggetarian"]},
        ],
        "snacks": [
            {"name": "Protein Shake", "ingredients": "Whey/plant protein, banana, peanut butter, milk", "calories": 350, "protein": "30g", "diet": ["veg", "eggetarian"]},
            {"name": "Vegan Protein Shake", "ingredients": "Plant protein, oat milk, banana, almond butter", "calories": 340, "protein": "28g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Cottage Cheese & Fruit", "ingredients": "1 cup cottage cheese, mixed berries", "calories": 220, "protein": "24g", "diet": ["veg"]},
            {"name": "Peanut Butter Banana Toast", "ingredients": "Whole-grain toast, 2 tbsp peanut butter, banana", "calories": 310, "protein": "12g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
        ],
    },
    "general_health": {
        "breakfast": [
            {"name": "Avocado Toast", "ingredients": "Whole-grain bread, avocado, poached egg, chili flakes", "calories": 380, "protein": "16g", "diet": ["veg", "eggetarian"]},
            {"name": "Berry Smoothie", "ingredients": "Mixed berries, banana, spinach, Greek yogurt, almond milk", "calories": 320, "protein": "14g", "diet": ["veg"]},
            {"name": "Muesli Bowl", "ingredients": "Rolled oats, dried fruits, nuts, seeds, yogurt", "calories": 360, "protein": "12g", "diet": ["veg"]},
            {"name": "Vegan Overnight Oats", "ingredients": "Rolled oats, oat milk, chia seeds, mixed berries, maple syrup", "calories": 340, "protein": "10g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
        ],
        "lunch": [
            {"name": "Mediterranean Bowl", "ingredients": "Falafel, hummus, tabbouleh, pita, cucumber, tomato", "calories": 480, "protein": "18g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Vegetable Soup & Bread", "ingredients": "Seasonal veggies, chickpeas, whole-grain bread", "calories": 380, "protein": "14g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Chicken Sandwich", "ingredients": "Grilled chicken, whole-grain bread, lettuce, tomato, mustard", "calories": 430, "protein": "32g", "diet": ["non-veg"]},
            {"name": "Stuffed Bell Peppers (Veg)", "ingredients": "Bell peppers, quinoa, black beans, corn, salsa, vegan cheese", "calories": 390, "protein": "16g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
        ],
        "dinner": [
            {"name": "Vegetable Stir-Fry & Tofu", "ingredients": "Firm tofu, mixed veggies, soy sauce, sesame oil, rice", "calories": 440, "protein": "22g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Pasta Primavera", "ingredients": "Whole-wheat pasta, seasonal vegetables, olive oil, parmesan", "calories": 460, "protein": "18g", "diet": ["veg"]},
            {"name": "Baked Chicken & Roasted Veggies", "ingredients": "Chicken breast, bell peppers, zucchini, herbs, olive oil", "calories": 420, "protein": "36g", "diet": ["non-veg"]},
            {"name": "Vegan Buddha Bowl", "ingredients": "Quinoa, roasted chickpeas, avocado, kale, tahini dressing", "calories": 430, "protein": "18g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
        ],
        "snacks": [
            {"name": "Trail Mix", "ingredients": "Mixed nuts, dried cranberries, dark chocolate chips (30g)", "calories": 170, "protein": "4g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Fruit Salad", "ingredients": "Seasonal fruits, mint leaves, lemon juice", "calories": 130, "protein": "2g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
            {"name": "Rice Cakes & Peanut Butter", "ingredients": "2 rice cakes, 1 tbsp peanut butter", "calories": 160, "protein": "5g", "diet": ["vegan", "veg", "eggetarian", "non-veg"]},
        ],
    },
}

HYDRATION_TIPS = [
    "💧 Drink at least 8 glasses (2 litres) of water daily.",
    "💧 Start your morning with a glass of warm water with lemon.",
    "💧 Drink 500ml of water 30 minutes before each workout.",
    "💧 Keep a water bottle visible at your desk as a constant reminder.",
    "💧 Herbal teas count toward your fluid intake — try chamomile or green tea.",
    "💧 Add cucumber or mint slices to water for a refreshing taste.",
    "💧 Drink water after every trip to the bathroom to maintain hydration.",
]

MACRO_GUIDANCE = {
    "weight_loss": {"calories": "1400–1700 kcal/day", "calories_min": 1400, "calories_max": 1700, "protein": "25–35%", "carbs": "40–45%", "fats": "20–30%"},
    "muscle_gain": {"calories": "2200–2800 kcal/day", "calories_min": 2200, "calories_max": 2800, "protein": "30–35%", "carbs": "45–50%", "fats": "15–25%"},
    "general_health": {"calories": "1800–2200 kcal/day", "calories_min": 1800, "calories_max": 2200, "protein": "20–30%", "carbs": "45–55%", "fats": "20–30%"},
}

# Diet preference resolution map
_DIET_ALIASES = {
    "vegetarian": "veg",
    "veg": "veg",
    "vegan": "vegan",
    "eggetarian": "eggetarian",
    "egg": "eggetarian",
    "non-veg": "non-veg",
    "nonveg": "non-veg",
    "non_veg": "non-veg",
    "meat": "non-veg",
}

# Diet fallback hierarchy: if a meal is not available for stricter diet, fall back
_DIET_FALLBACK = {
    "vegan": ["vegan", "veg"],
    "veg": ["veg", "eggetarian", "vegan"],
    "eggetarian": ["eggetarian", "veg"],
    "non-veg": ["non-veg", "veg", "eggetarian", "vegan"],
}


def _resolve_diet(diet_preference: str) -> str:
    """Normalise a diet string to one of: vegan, veg, eggetarian, non-veg."""
    return _DIET_ALIASES.get(diet_preference.lower().strip(), "non-veg")


def _filter_items_for_diet(items: list, diet: str) -> list:
    """Return items compatible with the given diet tag, using fallback hierarchy."""
    allowed_tags = _DIET_FALLBACK.get(diet, ["non-veg"])
    for tag in allowed_tags:
        filtered = [item for item in items if tag in item.get("diet", [])]
        if filtered:
            return filtered
    # Last resort: return all items
    return items


def get_meal_plan(goal: str, diet_preference: str = "non-veg") -> dict:
    """Return full meal plan for a given goal, filtered by dietary preference."""
    goal_map = {
        "weight_loss": "weight_loss",
        "lose_weight": "weight_loss",
        "muscle_gain": "muscle_gain",
        "build_muscle": "muscle_gain",
        "general": "general_health",
        "general_health": "general_health",
        "stay_healthy": "general_health",
    }
    resolved_goal = goal_map.get(goal.lower().replace(" ", "_"), "general_health")
    diet = _resolve_diet(diet_preference)
    raw_plan = MEAL_PLANS.get(resolved_goal, MEAL_PLANS["general_health"])

    filtered = {}
    for meal_time, items in raw_plan.items():
        filtered[meal_time] = _filter_items_for_diet(items, diet)
    return filtered


def format_meal_suggestion(goal: str, diet_preference: str = "non-veg") -> str:
    """Format a daily meal plan as readable markdown with dietary filtering."""
    import random
    plan = get_meal_plan(goal, diet_preference)
    macro_key = goal.lower().replace(" ", "_")
    macro_key = {
        "lose_weight": "weight_loss",
        "build_muscle": "muscle_gain",
        "general": "general_health",
        "stay_healthy": "general_health",
    }.get(macro_key, macro_key)
    macro = MACRO_GUIDANCE.get(macro_key, MACRO_GUIDANCE["general_health"])
    hydration = random.choice(HYDRATION_TIPS)
    diet_label = _resolve_diet(diet_preference).replace("-", " ").title()

    lines = [
        f"🥗 **Daily Meal Plan — {goal.replace('_', ' ').title()} ({diet_label})**",
        "",
        f"📊 *Daily Targets: {macro['calories']} · Protein {macro['protein']} · Carbs {macro['carbs']} · Fats {macro['fats']}*",
        "",
    ]
    emojis = {"breakfast": "🌅", "lunch": "☀️", "dinner": "🌙", "snacks": "🍎"}
    total_calories = 0
    for meal_time, items in plan.items():
        meal = random.choice(items)
        total_calories += meal["calories"]
        lines += [
            f"{emojis.get(meal_time, '🍽️')} **{meal_time.title()}:** {meal['name']}",
            f"   *{meal['ingredients']}*",
            f"   Calories: {meal['calories']} kcal · Protein: {meal['protein']}",
            "",
        ]
    lines += [
        f"🔢 **Total Daily Calories (sampled meals): ~{total_calories} kcal** *(target: {macro['calories']})*",
        "",
        hydration,
        "",
        "> ⚠️ *Nutritional values are estimates only. Individual needs vary. "
        "Consult a registered dietitian for personalised advice.*",
    ]
    return "\n".join(lines)
