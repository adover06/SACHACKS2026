"""
Substitution Expert: a focused LLM chain (not a full agent) that checks
missing ingredients and suggests UC Davis pantry-specific swaps.
"""

import json
import re

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from app.config import Settings

SYSTEM_PROMPT = """You are a Substitution Expert for the UC Davis ASUCD Pantry.

Given a recipe's ingredient list and the items currently available in the pantry,
determine the status of each ingredient and suggest substitutions for missing ones.

Rules:
- If the ingredient (or a close variant) is in the pantry list, mark it "available"
- If the ingredient is NOT in the pantry, mark it "missing" and suggest a substitution
- Substitutions MUST use ONLY items from the provided pantry list
- Use common cooking substitutions (e.g., applesauce for eggs, coconut oil for butter)
- Include the quantity in the substitution (e.g., "1/4 cup Applesauce")
- If no reasonable substitution exists, set substitution to null

Return ONLY a JSON array of objects:
[{"name": "Ingredient", "status": "available"|"missing", "substitution": "string or null"}]

Return ONLY the JSON array, no other text."""


async def run_substitution_check(
    recipe_ingredients: list[str],
    pantry_items: list[str],
    settings: Settings,
) -> list[dict]:
    """
    Run the substitution chain for a single recipe.

    Returns list of {"name": str, "status": "available"|"missing", "substitution": str|None}
    """
    llm = ChatOllama(
        model=settings.OLLAMA_TEXT_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0.2,
    )

    human_msg = (
        f"Recipe ingredients: {json.dumps(recipe_ingredients)}\n\n"
        f"Available pantry items: {json.dumps(pantry_items)}\n\n"
        "Analyze each recipe ingredient and return the JSON array."
    )

    response = await llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=human_msg),
    ])

    return _parse_substitution_response(response.content, recipe_ingredients, pantry_items)


def _parse_substitution_response(
    content: str,
    recipe_ingredients: list[str],
    pantry_items: list[str],
) -> list[dict]:
    """Parse LLM response, with fallback to rule-based matching."""
    # Try JSON parse
    try:
        items = json.loads(content)
        if isinstance(items, list):
            return _validate_substitutions(items)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON array
    match = re.search(r"\[.*\]", content, re.DOTALL)
    if match:
        try:
            items = json.loads(match.group())
            if isinstance(items, list):
                return _validate_substitutions(items)
        except json.JSONDecodeError:
            pass

    # Fallback: simple availability check (no LLM substitutions)
    pantry_lower = {p.strip().lower() for p in pantry_items}
    result = []
    for ing in recipe_ingredients:
        if ing.strip().lower() in pantry_lower:
            result.append({"name": ing, "status": "available", "substitution": None})
        else:
            result.append({"name": ing, "status": "missing", "substitution": None})
    return result


def _validate_substitutions(items: list) -> list[dict]:
    """Ensure each item has the required fields."""
    validated = []
    for item in items:
        if isinstance(item, dict) and "name" in item:
            validated.append({
                "name": str(item["name"]),
                "status": item.get("status", "missing"),
                "substitution": item.get("substitution"),
            })
    return validated
