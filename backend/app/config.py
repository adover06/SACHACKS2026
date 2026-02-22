from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Groq (cloud - primary for text)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    # Ollama (local - vision + text fallback)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_VISION_MODEL: str = "llava"
    OLLAMA_TEXT_MODEL: str = "llama3"

    # Notion
    NOTION_API_KEY: str = ""
    NOTION_PANTRY_DATABASE_ID: str = ""

    # Google Sheets
    GOOGLE_SERVICE_ACCOUNT_JSON: str = "credentials.json"
    GOOGLE_SHEETS_RECIPE_SPREADSHEET_ID: str = ""

    # App
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env"}


settings = Settings()
