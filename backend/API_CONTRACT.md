# Scan, Swap, Sustain — Backend API Contract

> **Base URL:** `http://localhost:8000`
> **Swagger UI:** `http://localhost:8000/docs`
> **Status:** All endpoints return JSON. CORS is enabled for `http://localhost:3000`.

---

## Endpoints

### 1. `GET /health`

Check if the backend and Ollama are running.

**Response:**
```json
{
  "status": "ok",
  "ollama": "connected",
  "ollama_url": "http://localhost:11434",
  "vision_model": "llava",
  "text_model": "llama3"
}
```

Use this on app load to show a connection status indicator. If `ollama` is `"unreachable"`, the scan and recipe endpoints will fail.

---

### 2. `POST /scan`

Upload a pantry/grocery image. The backend uses a vision LLM to identify food items and cross-references them with the ASUCD Pantry inventory.

**Request:** `multipart/form-data`

| Field   | Type   | Required | Description                |
|---------|--------|----------|----------------------------|
| `image` | File   | Yes      | JPEG/PNG image of pantry items |

**Example (fetch):**
```typescript
const formData = new FormData();
formData.append("image", file); // File from <input type="file"> or camera

const res = await fetch("http://localhost:8000/scan", {
  method: "POST",
  body: formData,
});
const data: ScanResponse = await res.json();
```

**Response (200):**
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "identified_items": [
    { "name": "Peanut Butter", "confidence": 0.98, "source": "ASUCD Pantry" },
    { "name": "Rice", "confidence": 0.95, "source": "ASUCD Pantry" },
    { "name": "Sriracha", "confidence": 0.82, "source": "Personal" }
  ],
  "suggested_filters": ["High Protein", "Quick (<15 min)", "Vegetarian"]
}
```

**Response fields:**

| Field               | Type     | Description |
|---------------------|----------|-------------|
| `session_id`        | string   | UUID — pass this to `/generate-recipes` |
| `identified_items`  | array    | Food items detected in the image |
| `identified_items[].name` | string | Item name |
| `identified_items[].confidence` | number (0-1) | Vision model confidence |
| `identified_items[].source` | string | `"ASUCD Pantry"` if in pantry inventory, `"Personal"` otherwise |
| `suggested_filters` | string[] | Suggested dietary/speed filters based on items |

**Errors:**
- `400` — Empty image file
- `502` — Vision model unreachable (Ollama down)

**Frontend notes:**
- This is the "Focus Moment" — show a skeleton/loading state while waiting (takes 3-10 seconds depending on GPU)
- After response, display the items list and let the user edit (add/remove items) before calling `/generate-recipes`
- The `source` field can be used to badge items (e.g., green badge for "ASUCD Pantry")

---

### 3. `POST /generate-recipes`

Generate recipe recommendations with the Substitution Engine and Academic Fuel scores.

**Request:** `application/json`

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "identified_items": ["Peanut Butter", "Rice", "Noodles", "Soy Sauce"],
  "filters": ["Vegetarian", "Quick (<15 min)"],
  "dietary_preferences": ["No Dairy"]
}
```

**Request fields:**

| Field                 | Type     | Required | Description |
|-----------------------|----------|----------|-------------|
| `session_id`          | string   | Yes      | UUID from the `/scan` response |
| `identified_items`    | string[] | Yes      | List of ingredient names (from scan or user-edited) |
| `filters`             | string[] | No       | Filters like `"Vegetarian"`, `"High Protein"`, `"Quick (<15 min)"`, `"No-Cook"` |
| `dietary_preferences` | string[] | No       | Allergies/restrictions like `"No Dairy"`, `"Gluten Free"` |

**Example (fetch):**
```typescript
const res = await fetch("http://localhost:8000/generate-recipes", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    session_id: scanData.session_id,
    identified_items: ["Peanut Butter", "Rice", "Noodles", "Soy Sauce"],
    filters: ["Vegetarian"],
    dietary_preferences: [],
  }),
});
const data: GenerateRecipesResponse = await res.json();
```

**Response (200):**
```json
{
  "recipes": [
    {
      "id": "recipe_001",
      "title": "Aggie Pad Thai",
      "academic_fuel_score": 8.5,
      "fuel_summary": "High in protein and complex carbs for sustained focus.",
      "ingredients": [
        { "name": "Peanut Butter", "status": "available", "substitution": null },
        { "name": "Noodles", "status": "available", "substitution": null },
        { "name": "Soy Sauce", "status": "available", "substitution": null },
        {
          "name": "Egg",
          "status": "missing",
          "substitution": "1/4 cup Applesauce (Available in Pantry)"
        }
      ],
      "instructions": [
        "Boil noodles according to package directions",
        "Mix peanut butter with soy sauce and a splash of water",
        "Toss noodles in the peanut sauce",
        "Add applesauce substitute and stir through"
      ]
    }
  ]
}
```

**Response fields:**

| Field | Type | Description |
|-------|------|-------------|
| `recipes` | array | Up to 5 recipe recommendations |
| `recipes[].id` | string | Unique recipe ID |
| `recipes[].title` | string | Recipe name |
| `recipes[].academic_fuel_score` | number (1-10) | Brain Power score — higher = better for studying |
| `recipes[].fuel_summary` | string | Human-readable nutrition summary |
| `recipes[].ingredients` | array | Ingredient list with availability status |
| `recipes[].ingredients[].name` | string | Ingredient name |
| `recipes[].ingredients[].status` | `"available"` \| `"missing"` | Whether the user has this ingredient |
| `recipes[].ingredients[].substitution` | string \| null | Pantry-available swap for missing items. `null` if available or no sub found |
| `recipes[].instructions` | string[] | Step-by-step cooking instructions |

**Errors:**
- `400` — No ingredients provided
- `502` — LLM or data source unreachable

**Frontend notes:**
- This call takes 5-15 seconds (LLM reasoning + data lookups) — use skeleton cards
- Sort/display recipes by `academic_fuel_score` descending (best brain fuel first)
- Color-code ingredients: green for `"available"`, orange/yellow for `"missing"` with substitution text
- The `fuel_summary` is a short string meant to display as a subtitle under the score

---

## TypeScript Types

Drop these into your frontend for type safety:

```typescript
// --- /scan ---

interface IdentifiedItem {
  name: string;
  confidence: number; // 0-1
  source: "ASUCD Pantry" | "Personal";
}

interface ScanResponse {
  session_id: string;
  identified_items: IdentifiedItem[];
  suggested_filters: string[];
}

// --- /generate-recipes ---

interface GenerateRecipesRequest {
  session_id: string;
  identified_items: string[];
  filters?: string[];
  dietary_preferences?: string[];
}

type IngredientStatus = "available" | "missing";

interface RecipeIngredient {
  name: string;
  status: IngredientStatus;
  substitution: string | null;
}

interface Recipe {
  id: string;
  title: string;
  academic_fuel_score: number; // 1-10
  fuel_summary: string;
  ingredients: RecipeIngredient[];
  instructions: string[];
}

interface GenerateRecipesResponse {
  recipes: Recipe[];
}

// --- /health ---

interface HealthResponse {
  status: string;
  ollama: "connected" | "unreachable";
  ollama_url: string;
  vision_model: string;
  text_model: string;
}
```

---

## App Flow (Frontend ↔ Backend)

```
1. App loads → GET /health → show connection status

2. User taps "Scan" → camera/upload → POST /scan (multipart)
   → Show skeleton while loading
   → Display identified_items list
   → Let user edit items (add/remove)
   → Show suggested_filters as toggleable chips

3. User confirms items + selects filters → POST /generate-recipes (JSON)
   → Show skeleton recipe cards while loading
   → Display recipe cards sorted by academic_fuel_score
   → Each card shows: title, score badge, fuel_summary, ingredient list, instructions
```

---

## Running the Backend

```bash
cd backend
cp .env.example .env              # Fill in Notion + Google Sheets keys
pip install -r requirements.txt
# On the machine with the RTX 4060:
ollama pull llava && ollama pull llama3
ollama serve                      # If not already running
# Start the API:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
