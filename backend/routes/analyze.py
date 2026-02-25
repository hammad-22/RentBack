"""API routes for the rent analysis endpoints."""

from fastapi import APIRouter, HTTPException
from backend.models import ApartmentInput, AnalysisResponse
from backend.scrapers.mock_data import generate_nyc_mock_comparables
from backend.scrapers.rentcast import RentCastScraper
from backend.analysis.market_analysis import analyze_market
from backend.ai.negotiation_generator import generate_negotiation
from backend.config import settings

router = APIRouter(prefix="/api")


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_apartment(apartment: ApartmentInput):
    """Main analysis endpoint.
    
    Takes apartment details, finds comparables, runs market analysis,
    and generates a negotiation script.
    """
    try:
        # Step 1: Get comparable listings
        comparables = []
        
        if settings.DATA_SOURCE == "rentcast" and settings.RENTCAST_API_KEY:
            try:
                scraper = RentCastScraper()
                comparables = await scraper.search(
                    address=apartment.address,
                    city=apartment.city,
                    state=apartment.state,
                    bedrooms=apartment.bedrooms,
                    radius_miles=settings.SEARCH_RADIUS_MILES,
                )
                print(f"[RentCast] Found {len(comparables)} real comparables")
            except Exception as e:
                print(f"[RentCast] API failed: {e}, falling back to mock data")
                comparables = []
        
        # Fallback to mock data if no real data was returned
        if not comparables:
            neighborhood = _extract_neighborhood(apartment.address, apartment.city)
            comparables = generate_nyc_mock_comparables(
                bedrooms=apartment.bedrooms,
                bathrooms=apartment.bathrooms,
                sqft=apartment.sqft,
                base_rent=apartment.current_rent,
                neighborhood=neighborhood,
            )
            print(f"[Mock] Generated {len(comparables)} mock comparables")
        
        # Step 2: Market analysis
        analysis = analyze_market(apartment, comparables)
        
        # Step 3: Generate negotiation script
        negotiation = await generate_negotiation(apartment, analysis, comparables)
        
        return AnalysisResponse(
            apartment=apartment,
            comparables=comparables,
            analysis=analysis,
            negotiation=negotiation,
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


def _extract_neighborhood(address: str, city: str) -> str:
    """Extract or guess neighborhood from address. Simplified for MVP."""
    address_lower = address.lower()
    
    # NYC neighborhoods based on street patterns
    if any(x in address_lower for x in ["e 6", "e 7", "e 8", "e 9", "e 1", "east"]):
        if any(x in address_lower for x in ["e 7", "e 8"]):
            return "Upper East Side"
        elif any(x in address_lower for x in ["e 6", "e 5", "e 4", "e 3"]):
            return "East Village"
    
    if any(x in address_lower for x in ["w 6", "w 7", "w 8", "w 9", "west"]):
        if any(x in address_lower for x in ["w 7", "w 8"]):
            return "Upper West Side"
        elif any(x in address_lower for x in ["w 1", "w 2"]):
            return "Chelsea"
    
    if any(x in address_lower for x in ["bedford", "williamsburg", "berry", "wythe"]):
        return "Williamsburg"
    
    if any(x in address_lower for x in ["bleecker", "christopher", "grove", "perry"]):
        return "West Village"
    
    return "Manhattan"


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "llm_provider": settings.LLM_PROVIDER,
        "data_source": settings.DATA_SOURCE,
    }
