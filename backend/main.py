"""FastAPI application entry point for the RentBack API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.routes.analyze import router as analyze_router
from backend.routes.stats import router as stats_router

app = FastAPI(
    title="RentBack API",
    description="AI-powered rent negotiation analysis and script generation",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(analyze_router)
app.include_router(stats_router)


@app.get("/")
async def root():
    return {
        "name": "RentBack API",
        "version": "1.0.0",
        "docs": "/docs",
    }
