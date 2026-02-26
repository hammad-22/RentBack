# RentBack

**AI-powered rent negotiation for NYC renters.** Analyzes comparable listings, adjusts for feature differences, and generates data-backed negotiation scripts to help you pay fair rent.

## How It Works

1. **Enter your apartment details** — address, bedrooms, bathrooms, current rent, amenities
2. **We find comparables** — real listings within 0.5 miles, matched by size and features
3. **Get your analysis** — feature-adjusted fair market rate with confidence scoring
4. **Negotiate with data** — personalized negotiation script with specific talking points

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16 (React 19), TypeScript (strict), CSS Modules |
| Backend | FastAPI (Python 3.12), Pydantic v2, Uvicorn |
| LLM | Multi-provider: OpenAI, Groq, Mistral, Ollama, mock fallback |
| Data | RentCast API for comparables, mock data fallback |
| Deploy | Netlify (frontend), Google Cloud Run via Docker (backend) |

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

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.12+

### Frontend

```bash
cd frontend
npm install
npm run dev     # → http://localhost:3000
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000   # → http://localhost:8000
```

API docs available at [http://localhost:8000/docs](http://localhost:8000/docs) when the backend is running.

### Docker Compose (Recommended)

Spin up both services with a single command — includes hot reloading:

```bash
docker compose up
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

Edit any file and changes reflect immediately (uvicorn `--reload` for backend, Next.js HMR for frontend).

Requires Docker and a `backend/.env` file (copy from `backend/.env.example`).

### Docker (Backend Only)

For production backend image (used by Cloud Run):

```bash
docker build -t rentback-api .
docker run -p 8080:8080 rentback-api
```

## Environment Variables

### Frontend (`.env.local`)

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |

### Backend (`.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | `openai` \| `groq` \| `mistral` \| `ollama` \| `mock` | `mock` |
| `DATA_SOURCE` | `mock` \| `rentcast` \| `scrape` | `mock` |
| `RENTCAST_API_KEY` | RentCast API key (required if `DATA_SOURCE=rentcast`) | — |
| `OPENAI_API_KEY` | OpenAI API key | — |
| `GROQ_API_KEY` | Groq API key | — |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:3000` |
| `SEARCH_RADIUS_MILES` | Comparable search radius | `0.5` |

Copy `.env.example` (backend) and `.env.local.example` (frontend) to get started.

## Architecture

```
┌─────────────┐     POST /api/analyze     ┌──────────────────┐
│   Next.js    │ ──────────────────────── │    FastAPI        │
│   Frontend   │                          │    Backend        │
│  (Netlify)   │ ◄──── AnalysisResponse ── │  (Cloud Run)     │
└─────────────┘                           └──────────────────┘
                                                   │
                                    ┌──────────────┼──────────────┐
                                    ▼              ▼              ▼
                              ┌──────────┐  ┌──────────┐  ┌──────────┐
                              │ RentCast │  │  Market  │  │   LLM    │
                              │   API    │  │ Analysis │  │ Provider │
                              └──────────┘  └──────────┘  └──────────┘
```

- **Stateless MVP** — No database. Results stored in frontend sessionStorage.
- **Market analysis** adjusts comparable rents by sqft ($2/sqft), floor level ($35/floor), and amenities ($25–$200 each), then computes a distance-weighted average.
- **Negotiation scripts** are template-based by default, LLM-powered when a provider is configured, and always fall back to templates on failure.
- **Address autocomplete** uses Nominatim (OpenStreetMap) with 400ms debounce.

## API

### `POST /api/analyze`

Accepts apartment details, returns comparable analysis and negotiation script.

**Request body:**
```json
{
  "address": "123 Main St",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001",
  "bedrooms": 1,
  "bathrooms": 1,
  "current_rent": 2800,
  "amenities": ["Doorman", "Gym"],
  "sqft": 650,
  "floor_level": 4,
  "building_type": "elevator"
}
```

**Response includes:** comparable listings, adjusted market rate, overpayment analysis, confidence score, negotiation strength, and a personalized negotiation script.

### `GET /api/stats`

Returns platform-level metrics (currently mock data).

## Hosting & Deployment

### Current Production Setup

- **Frontend:** Netlify — auto-deploys on push to main via GitHub integration
  - Domain: `rentback.nyc` (A record → 75.2.60.5, Netlify load balancer)
  - Config: `netlify.toml` (build command: `npm run build`, publish: `.next`)
- **Backend:** Google Cloud Run — containerized, us-east4 region
  - Domain: `api.rentback.nyc` (CNAME → ghs.googlehosted.com)
  - Scales to zero when idle (cost-efficient for low traffic)
  - SSL auto-provisions via Cloud Run

### Deploying Changes

**Frontend** deploys automatically when you push to the main branch (Netlify watches the repo).

**Backend** requires manual deployment — no CI/CD pipeline yet:

```bash
# Build and push the Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/rentback-api .
docker push gcr.io/YOUR_PROJECT_ID/rentback-api

# Deploy to Cloud Run
gcloud run deploy rentback-api \
  --image gcr.io/YOUR_PROJECT_ID/rentback-api \
  --region us-east4 \
  --platform managed
```

### Production Environment Variables

**Frontend (Netlify):**
```
NEXT_PUBLIC_API_URL=https://api.rentback.nyc
```

**Backend (Cloud Run):**
```
CORS_ORIGINS=https://rentback.nyc
LLM_PROVIDER=groq
GROQ_API_KEY=...
DATA_SOURCE=rentcast
RENTCAST_API_KEY=...
```

### Hosting Alternatives

If the current setup needs to change:

- **Railway** — Single platform for both frontend + backend, ~$10–15/month at hobby scale, auto-deploys on git push
- **Render** — Free tier available (cold starts on free plan, use paid tier for production)
- **Fly.io** — Global edge deployment if latency becomes a concern

### Database

Not required for the current MVP. The app is fully stateless — RentCast and Groq are called on demand, results pass through sessionStorage client-side.

**When to add one:**
- User accounts and saved report history
- Real aggregated homepage stats (currently mock constants from `/api/stats`)
- RentCast result caching (their API has call limits; caching by address + bedroom count avoids redundant calls)
- Lease renewal reminders and alerts

**Recommended:** Supabase (PostgreSQL) — free tier, managed, works alongside any hosting provider.

## Code Conventions

- **Frontend:** PascalCase components/types, camelCase functions. CSS Modules. `"use client"` on interactive pages. Path alias `@/*` → `./src/*`.
- **Backend:** snake_case functions/variables, PascalCase classes. Async endpoints. HTTPException for errors with fallbacks.
- **Type sync:** Frontend types in `lib/api.ts` must stay in sync with backend models in `models.py`.
- **Styling:** CSS custom properties in `globals.css`. Fonts: Cormorant Garamond (headings), Inter (body). Minimal palette: black/white primary, green/orange/red status.

## Scripts

| Command | Location | Description |
|---------|----------|-------------|
| `npm run dev` | `frontend/` | Start Next.js dev server |
| `npm run build` | `frontend/` | Production build |
| `npm run lint` | `frontend/` | Run ESLint |
| `uvicorn backend.main:app --reload --port 8000` | `backend/` | Start FastAPI dev server |
| `docker compose up` | root | Start frontend + backend with hot reload |
| `docker build -t rentback-api .` | root | Build production backend Docker image |

## Notes

- Groq is free tier for now — switch to Anthropic Claude or OpenAI if quality needs upgrade
- Avoid Vercel for frontend hosting — use Netlify
- Keep backend on Cloud Run (scales to zero = cheap)

## License

All rights reserved.
