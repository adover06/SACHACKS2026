"""
LangChain tool: query ASUCD Pantry inventory from Notion.
"""

import json
from langchain_core.tools import tool
from notion_client import AsyncClient

from app.config import settings


_notion = AsyncClient(auth=settings.NOTION_API_KEY) if settings.NOTION_API_KEY else None


@tool
async def query_pantry_inventory(category: str = "") -> str:
    """Query the ASUCD Pantry Notion database for currently available items.
    Optionally filter by category (e.g., 'Protein', 'Grains', 'Dairy').
    Returns a JSON list of available pantry items."""

    if not _notion:
        return json.dumps({"error": "Notion API key not configured"})

    filter_params = {}
    if category:
        filter_params = {
            "filter": {
                "property": "Category",
                "select": {"equals": category},
            }
        }

    results = await _notion.databases.query(
        database_id=settings.NOTION_PANTRY_DATABASE_ID,
        **filter_params,
    )

    items = []
    for page in results["results"]:
        props = page["properties"]
        try:
            name = props["Name"]["title"][0]["plain_text"]
            cat = props.get("Category", {}).get("select", {}).get("name", "Unknown")
            available = props.get("Available", {}).get("checkbox", True)
            quantity = props.get("Quantity", {}).get("number")

            if available:
                items.append({
                    "name": name,
                    "category": cat,
                    "quantity": quantity,
                })
        except (KeyError, IndexError):
            continue

    return json.dumps(items)
