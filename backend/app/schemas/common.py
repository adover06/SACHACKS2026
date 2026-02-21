from enum import Enum


class IngredientStatus(str, Enum):
    available = "available"
    missing = "missing"
