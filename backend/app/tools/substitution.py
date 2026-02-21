"""
LangChain tool: wraps the Substitution Expert chain as a callable tool.
"""

import json
from langchain_core.tools import tool

from app.agents.substitution_expert import run_substitution_check as _run_check
from app.config import settings


@tool
async def run_substitution_check(recipe_ingredients: str, pantry_items: str) -> str:
    """Check which recipe ingredients are available in the pantry and suggest
    substitutions for missing ones using UC Davis pantry-specific swaps.

    Args:
        recipe_ingredients: JSON string of ingredient names for a recipe
        pantry_items: JSON string of available pantry item names
    """
    try:
        ingredients = json.loads(recipe_ingredients)
        pantry = json.loads(pantry_items)
    except json.JSONDecodeError:
        ingredients = [i.strip() for i in recipe_ingredients.split(",")]
        pantry = [i.strip() for i in pantry_items.split(",")]

    result = await _run_check(
        recipe_ingredients=ingredients,
        pantry_items=pantry,
        settings=settings,
    )
    return json.dumps(result)
