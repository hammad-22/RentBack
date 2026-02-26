# RentBack

AI-powered rent negotiation platform for NYC renters. Analyzes comparable listings, adjusts for feature differences, and generates data-backed negotiation scripts.

## Tech Stack

- **Frontend:** Next.js 16 (React 19), TypeScript (strict), CSS Modules
- **Backend:** FastAPI (Python 3.12), Pydantic v2, Uvicorn
- **LLM:** Multi-provider (OpenAI, Groq, Mistral, Ollama, mock fallback)
- **Data:** RentCast API for comparables, mock data fallback
- **Deploy:** Netlify (frontend), Google Cloud Run via Docker (backend)

## Project Structure

```
frontend/src/
  app/
    page.tsx                  # Homepage
    analyze/page.tsx          # Analysis form (address autocomplete, unit details)
    results/page.tsx          # Results display (report, comparables, negotiation)
  components/NYCSkyline.tsx   # Decorative SVG background
  lib/api.ts                  # API client + TypeScript types

backend/
  main.py                     # FastAPI app, CORS, route mounting
  config.py                   # Pydantic Settings from env vars
  models.py                   # Pydantic request/response models
  routes/analyze.py           # POST /api/analyze
  routes/stats.py             # GET /api/stats
  analysis/market_analysis.py # Comparative market analysis engine
  ai/negotiation_generator.py # LLM-powered + template negotiation scripts
  scrapers/                   # rentcast.py, mock_data.py, base.py
```

## Commands

### Frontend
```bash
cd frontend && npm install        # Install deps
npm run dev                       # Dev server on :3000
npm run build                     # Production build
npm run lint                      # ESLint
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000   # Dev server on :8000, docs at /docs
```

### Docker
```bash
docker build -t rentback-api .
docker run -p 8080:8080 rentback-api
```

## Environment Variables

**Frontend** (`.env.local`): `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000`)

**Backend** (`.env`):
- `LLM_PROVIDER`: openai | groq | mistral | ollama | mock (default: mock)
- `DATA_SOURCE`: mock | rentcast | scrape (default: mock)
- `RENTCAST_API_KEY`, `OPENAI_API_KEY`, `GROQ_API_KEY`: API keys
- `CORS_ORIGINS`: Comma-separated allowed origins
- `SEARCH_RADIUS_MILES`: Comparable search radius (default: 0.5)

## Code Conventions

- **Frontend:** PascalCase components/types, camelCase functions. CSS Modules with descriptive class names. `"use client"` on interactive pages. Path alias `@/*` maps to `./src/*`.
- **Backend:** snake_case functions/variables, PascalCase classes. Async endpoints. HTTPException for errors with fallbacks. Keep frontend types (`lib/api.ts`) in sync with backend models (`models.py`).
- **Styling:** CSS custom properties in `globals.css`. Fonts: Cormorant Garamond (headings), Inter (body). Minimal color palette: black/white primary, green/orange/red status.

## Architecture Notes

- Stateless MVP: no database, results stored in frontend sessionStorage
- Market analysis adjusts comparable rents by sqft ($2/sqft), floor ($35/floor), amenities ($25-$200 each), then distance-weighted average
- Negotiation generation: template-based by default, LLM-powered when provider configured, always falls back to template on failure
- Address autocomplete uses Nominatim (OpenStreetMap) API with 400ms debounce
