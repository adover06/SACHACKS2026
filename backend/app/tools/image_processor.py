"""
Vision tool: analyze pantry images using ChatOllama + llava.
"""

import base64
import json
import re

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

from app.config import Settings


async def analyze_pantry_image(image_bytes: bytes, settings: Settings) -> list[dict]:
    """
    Send a pantry image to llava via Ollama and return identified food items.

    Returns list of {"name": str, "confidence": float}.
    """
    llm = ChatOllama(
        model=settings.OLLAMA_VISION_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0,
    )

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": (
                    "You are a food identification assistant. Identify ALL food items "
                    "visible in this pantry/grocery image. Return ONLY a JSON array of "
                    "objects, each with 'name' (string, the food item) and 'confidence' "
                    "(float 0-1, how confident you are). Example:\n"
                    '[{"name": "Peanut Butter", "confidence": 0.95}]\n'
                    "Return ONLY the JSON array, no other text."
                ),
            },
            {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{image_b64}",
            },
        ]
    )

    response = await llm.ainvoke([message])
    return _parse_items_response(response.content)


def _parse_items_response(content: str) -> list[dict]:
    """Parse LLM response into a list of identified items."""
    # Try direct JSON parse
    try:
        items = json.loads(content)
        if isinstance(items, list):
            return _validate_items(items)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON array from surrounding text
    match = re.search(r"\[.*\]", content, re.DOTALL)
    if match:
        try:
            items = json.loads(match.group())
            if isinstance(items, list):
                return _validate_items(items)
        except json.JSONDecodeError:
            pass

    return []


def _validate_items(items: list) -> list[dict]:
    """Ensure each item has name and confidence fields."""
    validated = []
    for item in items:
        if isinstance(item, dict) and "name" in item:
            validated.append({
                "name": str(item["name"]),
                "confidence": float(item.get("confidence", 0.7)),
            })
    return validated
