import time
import json
from notion_client import AsyncClient


class PantryCache:
    """In-memory TTL cache for Notion pantry inventory."""

    def __init__(self, ttl_seconds: int = 300):
        self._cache: list[dict] | None = None
        self._last_fetch: float = 0
        self._ttl = ttl_seconds

    @property
    def is_stale(self) -> bool:
        return self._cache is None or (time.time() - self._last_fetch) > self._ttl

    async def get_items(self, notion: AsyncClient, database_id: str) -> list[dict]:
        if self.is_stale:
            self._cache = await self._fetch(notion, database_id)
            self._last_fetch = time.time()
        return self._cache

    async def _fetch(self, notion: AsyncClient, database_id: str) -> list[dict]:
        results = await notion.databases.query(database_id=database_id)
        items = []
        for page in results["results"]:
            props = page["properties"]
            try:
                name = props["Name"]["title"][0]["plain_text"]
                category = props.get("Category", {}).get("select", {}).get("name", "Unknown")
                available = props.get("Available", {}).get("checkbox", True)
                quantity = props.get("Quantity", {}).get("number")
                items.append({
                    "name": name,
                    "category": category,
                    "available": available,
                    "quantity": quantity,
                })
            except (KeyError, IndexError):
                continue
        return [i for i in items if i["available"]]

    def get_item_names(self) -> set[str]:
        if self._cache is None:
            return set()
        return {item["name"].lower() for item in self._cache}

    def invalidate(self):
        self._cache = None
