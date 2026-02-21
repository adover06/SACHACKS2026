SYSTEM ROLE: You are an Elite Backend Architect specializing in FastAPI, LangChain, and Agentic Workflows. Your goal is to build the backend for "Scan, Swap, Sustain," a food equity app for UC Davis students.

OBJECTIVE: Build a production-ready FastAPI backend that processes pantry images, queries a recipe spreadsheet, and uses an AI "Substitution Engine" to suggest meals based on available ingredients.

TECH STACK:

Framework: FastAPI

Orchestration: LangChain (Agentic workflow for tool calling)

Data Sources: Notion API (Pantry status), Google Sheets (Scraped Recipes), Image Uploads (Vision-enabled LLM). 

Core Logic: "Substitution Engine" and "Academic Fuel" scoring.

PROJECT REPOSITORY STRUCTURE:

/app/main.py - Entry point and API routing.

/app/agents/ - LangChain agent definitions (Planner, Substitution Expert).

/app/tools/ - Custom tools for Notion, Google Sheets, and Image Processing.

/app/schemas/ - Pydantic models for request/response (JSON structure).

/app/services/ - Logic for "Academic Fuel" scoring.

SPECIFIC TASK INSTRUCTIONS:

Agentic Workflow: Use a LangChain agent to decide when to call the "Substitution Tool" vs. the "Recipe Database Tool."

The Substitution Engine: This tool must logic-check missing ingredients and suggest UC Davis pantry-specific swaps (e.g., apple sauce for eggs).

Academic Fuel Logic: Create a service that calculates a 1-10 "Brain Power" score based on protein, Omega-3s, and complex carbs.

Data Scraping: Provide a modular function to ingest the pantry spreadsheet data.

No Frontend: Focus strictly on the API endpoints and JSON responses.

DELIVERABLES:

Full Python code for the FastAPI structure.

Implementation of the LangChain Agent and Tools.

Detailed JSON Schemas for every endpoint so the Frontend Architect can begin integration immediately.

JSON Schemas for Coordination
To help you coordinate with your frontend architect right now, here are the core schemas that Claude will generate based on the prompt above.

1. Image Upload & Analysis (/scan)
This is the "Focus Moment" response.

JSON
{
  "session_id": "uuid-string",
  "identified_items": [
    {"name": "Peanut Butter", "confidence": 0.98, "source": "ASUCD Pantry"},
    {"name": "Rice", "confidence": 0.95, "source": "Pantry Staple"}
  ],
  "suggested_filters": ["Vegetarian", "High Protein", "Quick (<15 min)"]
}
2. Recipe Recommendations (/generate-recipes)
This includes the Substitution Engine and Academic Fuel score.

JSON
{
  "recipes": [
    {
      "id": "recipe_001",
      "title": "Aggie Pad Thai",
      "academic_fuel_score": 8.5,
      "fuel_summary": "High in healthy fats for long CS labs.",
      "ingredients": [
        {"name": "Peanut Butter", "status": "available"},
        {"name": "Noodles", "status": "available"},
        {
          "name": "Egg", 
          "status": "missing",
          "substitution": "1/4 cup Applesauce (Available in Pantry)"
        }
      ],
      "instructions": ["Boil noodles...", "Mix pantry peanut butter with soy sauce..."]
    }
  ]
}



PROJECT BLUEPRINT: [INSERT NAME] (SacHacks 2026)
🎯 1. MISSION & PROBLEM STATEMENT
Challenge: ASUCD Pantry: Pantry Recipe Website.
Goal: Bridge the gap between "Food Access" (having staples) and "Food Preparation" (making meals) for UC Davis students.
Redemption Arc: Moving from a "plain" v1 to a high-polish, Agentic RAG platform that prioritizes "Academic Fuel" and student autonomy.
Primary Tracks: 1.  Best Design (With Code)
2.  Best Social Good / Equity Project
3.  Overall Excellence
🎨 2. FRONTEND ARCHITECT REQUIREMENTS (Lead: YOU)
Tech Stack: Next.js 16 (App Router), TypeScript, Tailwind CSS v4.

UI/UX Style Guide (The "11x Winner" Rules)
Spacing: 8pt grid system only (Tailwind increments: p-2, p-4, p-8 / 8px, 16px, 32px).
Layout: Max content width 1100px (max-w-5xl mx-auto). No full-width stretching.
Typography: Single font family, line-height 1.4–1.6 for a premium feel.
Elements: * One primary button style (consistent radius/color).
Tap targets ≥ 44px height.
Spacing > Borders (fewer lines, more white space).
Interactivity:
Focus Moment: Hero-centric landing page (Camera Scan).
States: Hover, Active, Disabled, Loading (Skeleton screens).
Skeletons: Use loading.tsx for all AI/Scan states. Spinners are prohibited.
⚙️ 3. BACKEND ARCHITECT REQUIREMENTS (Lead: Andrew)
Tech Stack: FastAPI, LangChain, Python.

Core Logic: The "Agentic RAG" Engine
The Substitution Engine: An AI Agent that logic-checks missing ingredients and suggests UC Davis pantry-specific swaps (e.g., apple sauce for eggs).
Academic Fuel Logic: A service calculating a 1-10 "Brain Power" score based on protein, Omega-3s, and complex carbs for student success.
Data Ingestion: Scrape/Fetch daily inventory from the ASUCD Pantry Notion and reference the Pantry Recipes Spreadsheet.
🤝 4. THE API CONTRACT (The Bridge)
Both architects must strictly follow these schemas to ensure parallel development.

A. Scan Results (POST /scan)
JSON
{
  "session_id": "uuid-string",
  "identified_items": [
    {"name": "Peanut Butter", "confidence": 0.98, "source": "ASUCD Pantry"},
    {"name": "Rice", "confidence": 0.95, "source": "Pantry Staple"}
  ],
  "suggested_filters": ["Vegetarian", "High Protein", "No-Cook"]
}
B. Recipe Generation (POST /generate-recipes)
JSON
{
  "recipes": [
    {
      "id": "recipe_001",
      "title": "Aggie Pad Thai",
      "academic_fuel_score": 8.5,
      "fuel_summary": "High in healthy fats for long CS labs.",
      "ingredients": [
        {"name": "Peanut Butter", "status": "available"},
        {"name": "Egg", "status": "missing", "substitution": "1/4 cup Applesauce"}
      ],
      "instructions": ["Boil noodles...", "Mix peanut butter with soy sauce..."]
    }
  ]
}
🚀 5. MAIN APP FLOW
Auth (Optional/Guest): Firebase Login or Guest continue.
Scan (Focus Moment): User takes a photo of pantry haul.
Review: identified items list + "Add Aggie Staples" toggle.
Preferences: User selects Cuisine/Allergies/Health Goal.
Results: Recipes with Substitution Engine logic + Academic Fuel scores.