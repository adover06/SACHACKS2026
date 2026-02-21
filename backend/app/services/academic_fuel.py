"""
Academic Fuel scoring service.
Calculates a 1-10 "Brain Power" score based on protein, Omega-3s, and complex carbs.
Pure Python — no LLM dependency.
"""

NUTRIENT_PROFILES: dict[str, dict[str, float]] = {
    # Proteins
    "peanut butter": {"protein": 7, "omega3": 0.5, "complex_carbs": 2, "fiber": 2},
    "egg": {"protein": 6, "omega3": 0.3, "complex_carbs": 0, "fiber": 0},
    "eggs": {"protein": 6, "omega3": 0.3, "complex_carbs": 0, "fiber": 0},
    "chicken": {"protein": 9, "omega3": 0.1, "complex_carbs": 0, "fiber": 0},
    "tuna": {"protein": 8, "omega3": 2.5, "complex_carbs": 0, "fiber": 0},
    "salmon": {"protein": 9, "omega3": 3.0, "complex_carbs": 0, "fiber": 0},
    "tofu": {"protein": 5, "omega3": 0.4, "complex_carbs": 1, "fiber": 0.5},
    "beans": {"protein": 7, "omega3": 0.3, "complex_carbs": 6, "fiber": 6},
    "black beans": {"protein": 7, "omega3": 0.3, "complex_carbs": 6, "fiber": 6},
    "lentils": {"protein": 8, "omega3": 0.2, "complex_carbs": 7, "fiber": 7},
    "chickpeas": {"protein": 6, "omega3": 0.2, "complex_carbs": 5, "fiber": 5},
    # Grains & Carbs
    "rice": {"protein": 2, "omega3": 0, "complex_carbs": 8, "fiber": 1},
    "brown rice": {"protein": 3, "omega3": 0, "complex_carbs": 9, "fiber": 3},
    "oats": {"protein": 5, "omega3": 0.1, "complex_carbs": 9, "fiber": 4},
    "oatmeal": {"protein": 5, "omega3": 0.1, "complex_carbs": 9, "fiber": 4},
    "pasta": {"protein": 3, "omega3": 0, "complex_carbs": 7, "fiber": 2},
    "noodles": {"protein": 3, "omega3": 0, "complex_carbs": 7, "fiber": 1},
    "bread": {"protein": 3, "omega3": 0, "complex_carbs": 6, "fiber": 2},
    "whole wheat bread": {"protein": 4, "omega3": 0.1, "complex_carbs": 8, "fiber": 4},
    "tortilla": {"protein": 2, "omega3": 0, "complex_carbs": 5, "fiber": 1},
    # Fats & Oils
    "olive oil": {"protein": 0, "omega3": 0.8, "complex_carbs": 0, "fiber": 0},
    "coconut oil": {"protein": 0, "omega3": 0, "complex_carbs": 0, "fiber": 0},
    "butter": {"protein": 0, "omega3": 0.3, "complex_carbs": 0, "fiber": 0},
    # Dairy & Alternatives
    "milk": {"protein": 3, "omega3": 0.1, "complex_carbs": 1, "fiber": 0},
    "cheese": {"protein": 5, "omega3": 0.2, "complex_carbs": 0, "fiber": 0},
    "yogurt": {"protein": 4, "omega3": 0.1, "complex_carbs": 1, "fiber": 0},
    # Fruits & Vegetables
    "banana": {"protein": 1, "omega3": 0.1, "complex_carbs": 5, "fiber": 3},
    "apple": {"protein": 0, "omega3": 0, "complex_carbs": 3, "fiber": 2},
    "applesauce": {"protein": 0, "omega3": 0, "complex_carbs": 3, "fiber": 1},
    "spinach": {"protein": 1, "omega3": 0.4, "complex_carbs": 1, "fiber": 2},
    "broccoli": {"protein": 2, "omega3": 0.1, "complex_carbs": 2, "fiber": 3},
    "sweet potato": {"protein": 1, "omega3": 0, "complex_carbs": 8, "fiber": 4},
    "potato": {"protein": 1, "omega3": 0, "complex_carbs": 6, "fiber": 2},
    "tomato": {"protein": 1, "omega3": 0, "complex_carbs": 1, "fiber": 1},
    "carrot": {"protein": 0, "omega3": 0, "complex_carbs": 3, "fiber": 3},
    "onion": {"protein": 0, "omega3": 0, "complex_carbs": 2, "fiber": 1},
    "garlic": {"protein": 0, "omega3": 0, "complex_carbs": 1, "fiber": 0},
    # Nuts & Seeds
    "almonds": {"protein": 6, "omega3": 0.3, "complex_carbs": 2, "fiber": 4},
    "walnuts": {"protein": 4, "omega3": 2.5, "complex_carbs": 1, "fiber": 2},
    "chia seeds": {"protein": 3, "omega3": 5.0, "complex_carbs": 2, "fiber": 10},
    "flax seeds": {"protein": 3, "omega3": 6.0, "complex_carbs": 1, "fiber": 8},
    # Condiments & Misc
    "soy sauce": {"protein": 1, "omega3": 0, "complex_carbs": 0, "fiber": 0},
    "honey": {"protein": 0, "omega3": 0, "complex_carbs": 4, "fiber": 0},
    "sugar": {"protein": 0, "omega3": 0, "complex_carbs": 0, "fiber": 0},
    "salt": {"protein": 0, "omega3": 0, "complex_carbs": 0, "fiber": 0},
}


def calculate_academic_fuel_score(
    ingredient_names: list[str],
) -> tuple[float, str]:
    """
    Calculate a 1-10 "Brain Power" score.

    Formula:
      protein_score     = min(total_protein / 20, 1.0) * 4   (40% weight)
      omega3_score      = min(total_omega3 / 2.0, 1.0) * 3   (30% weight)
      complex_carb_score = min(total_carbs / 15, 1.0) * 3    (30% weight)

    Returns (score, summary_string).
    """
    total_protein = 0.0
    total_omega3 = 0.0
    total_carbs = 0.0

    for name in ingredient_names:
        key = name.strip().lower()
        profile = NUTRIENT_PROFILES.get(key)
        if profile:
            total_protein += profile["protein"]
            total_omega3 += profile["omega3"]
            total_carbs += profile["complex_carbs"]

    protein_score = min(total_protein / 20, 1.0) * 4
    omega3_score = min(total_omega3 / 2.0, 1.0) * 3
    carb_score = min(total_carbs / 15, 1.0) * 3

    final = round(protein_score + omega3_score + carb_score, 1)
    final = max(1.0, min(10.0, final))

    highlights = []
    if protein_score > 2.5:
        highlights.append("protein")
    if omega3_score > 2.0:
        highlights.append("Omega-3s")
    if carb_score > 2.0:
        highlights.append("complex carbs")

    if highlights:
        summary = f"High in {' and '.join(highlights)} for sustained focus."
    elif final >= 5.0:
        summary = "A solid balanced meal for steady energy."
    else:
        summary = "A light meal — consider adding protein or whole grains."

    return final, summary
