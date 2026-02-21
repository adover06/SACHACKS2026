"""
LangChain tool: search recipe database from Google Sheets.
"""

import json
import asyncio
from functools import lru_cache

import gspread
from google.oauth2.service_account import Credentials
from langchain_core.tools import tool

from app.config import settings

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def _get_sheet():
    creds = Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_JSON, scopes=SCOPES
    )
    gc = gspread.authorize(creds)
    return gc.open_by_key(settings.GOOGLE_SHEETS_RECIPE_SPREADSHEET_ID).sheet1


def _fetch_all_recipes() -> list[dict]:
    """Fetch all recipes from the spreadsheet (sync)."""
    sheet = _get_sheet()
    return sheet.get_all_records()


def _search_recipes_sync(ingredients: list[str], max_results: int = 5) -> list[dict]:
    """Search recipes by ingredient match percentage."""
    all_recipes = _fetch_all_recipes()
    available = {i.strip().lower() for i in ingredients}

    scored = []
    for recipe in all_recipes:
        # Expect a column called "ingredients" with comma-separated values
        raw_ingredients = recipe.get("ingredients", "")
        recipe_ingredients = [i.strip().lower() for i in raw_ingredients.split(",")]

        if not recipe_ingredients or not recipe_ingredients[0]:
            continue

        match_count = len(set(recipe_ingredients) & available)
        match_pct = match_count / len(recipe_ingredients)

        scored.append({
            "id": str(recipe.get("id", "")),
            "title": recipe.get("title", "Untitled"),
            "ingredients_raw": raw_ingredients,
            "instructions_raw": recipe.get("instructions", ""),
            "match_pct": round(match_pct, 2),
            "match_count": match_count,
            "total_ingredients": len(recipe_ingredients),
        })

    scored.sort(key=lambda x: x["match_pct"], reverse=True)
    return scored[:max_results]


@tool
async def query_recipe_database(ingredients: list[str], max_results: int = 5) -> str:
    """Search the recipe spreadsheet for recipes matching the given ingredients.
    Returns recipes sorted by how many ingredients match.
    Args:
        ingredients: list of available ingredient names
        max_results: max number of recipes to return (default 5)
    """
    results = await asyncio.to_thread(_search_recipes_sync, ingredients, max_results)
    return json.dumps(results)
