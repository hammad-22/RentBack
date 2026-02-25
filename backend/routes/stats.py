"""Platform statistics endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/api/stats")
async def get_stats():
    """Return platform-level statistics for the homepage.

    These are currently research-backed constants. Once a database is added,
    this endpoint should aggregate from real analysis history.
    """
    return {
        "avg_annual_savings": 2847,
        "avg_overpayment_rate": 14,
        "neighborhoods_covered": 8,
    }
