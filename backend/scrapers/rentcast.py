"""RentCast API scraper for real NYC rental comparables."""

import math
import httpx
from backend.models import ComparableListing
from backend.scrapers.base import BaseScraper
from backend.config import settings


def _haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two lat/lon points in miles."""
    R = 3958.8  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))


class RentCastScraper(BaseScraper):
    """Fetches real rental listings from the RentCast API."""

    BASE_URL = "https://api.rentcast.io/v1"

    @property
    def source_name(self) -> str:
        return "rentcast"

    async def search(
        self,
        address: str,
        city: str,
        state: str,
        bedrooms: int,
        radius_miles: float = 0.5,
    ) -> list[ComparableListing]:
        """Search RentCast for comparable rental listings near the given address."""

        params = {
            "address": f"{address}, {city}, {state}",
            "radius": radius_miles,
            "bedrooms": str(bedrooms),
            "status": "Active",
            "limit": 20,
            "daysOld": "90",
        }

        headers = {
            "accept": "application/json",
            "X-Api-Key": settings.RENTCAST_API_KEY,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/listings/rental/long-term",
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

        # RentCast returns a list of listing objects
        listings = data if isinstance(data, list) else data.get("listings", data.get("data", []))

        # Get the origin lat/lon from the first listing for distance calc
        origin_lat = None
        origin_lon = None
        if listings:
            # Use the search address's approximate location from first result
            # (we'll compute relative distances)
            all_lats = [item.get("latitude", 0) for item in listings if item.get("latitude")]
            all_lons = [item.get("longitude", 0) for item in listings if item.get("longitude")]
            if all_lats and all_lons:
                origin_lat = sum(all_lats) / len(all_lats)
                origin_lon = sum(all_lons) / len(all_lons)

        comparables = []
        for item in listings:
            try:
                comp = self._parse_listing(item, origin_lat, origin_lon)
                if comp:
                    comparables.append(comp)
            except Exception as e:
                print(f"[RentCast] Skipping listing: {e}")
                continue

        return comparables

    def _parse_listing(
        self,
        item: dict,
        origin_lat: float | None,
        origin_lon: float | None,
    ) -> ComparableListing | None:
        """Convert a RentCast API listing to our ComparableListing model."""

        rent = item.get("price") or item.get("rent") or item.get("listPrice")
        if not rent or float(rent) <= 0:
            return None

        # Use formattedAddress directly — it already includes city/state/zip
        full_address = (
            item.get("formattedAddress")
            or f"{item.get('addressLine1', '')}, {item.get('city', '')}, {item.get('state', '')} {item.get('zipCode', '')}".strip()
        )

        # Calculate distance from origin using lat/lon
        distance = 0.0
        lat = item.get("latitude")
        lon = item.get("longitude")
        if lat and lon and origin_lat and origin_lon:
            distance = round(_haversine_miles(origin_lat, origin_lon, lat, lon), 2)

        # Amenities from features
        amenities = []
        features = item.get("features", []) or []
        if isinstance(features, list):
            amenities = [str(f) for f in features]
        elif isinstance(features, dict):
            amenities = [k for k, v in features.items() if v]

        return ComparableListing(
            address=full_address or "Unknown Address",
            distance_miles=distance,
            rent=float(rent),
            bedrooms=int(item.get("bedrooms", 0) or 0),
            bathrooms=float(item.get("bathrooms", 1) or 1),
            sqft=int(item["squareFootage"]) if item.get("squareFootage") else None,
            floor_level=None,
            amenities=amenities,
            building_type=item.get("propertyType"),
            listing_url=item.get("listingUrl") or item.get("url"),
            source="rentcast",
            description=item.get("description"),
            date_listed=item.get("listedDate") or item.get("createdDate"),
        )
