"""Abstract base scraper interface."""

from abc import ABC, abstractmethod
from backend.models import ComparableListing


class BaseScraper(ABC):
    """Base class for all rental listing scrapers."""
    
    @abstractmethod
    async def search(
        self,
        address: str,
        city: str,
        state: str,
        bedrooms: int,
        radius_miles: float = 0.5,
    ) -> list[ComparableListing]:
        """Search for comparable rental listings.
        
        Args:
            address: Street address to search around
            city: City name
            state: State abbreviation
            bedrooms: Number of bedrooms to filter by
            radius_miles: Search radius in miles
            
        Returns:
            List of comparable listings found
        """
        pass
    
    @property
    @abstractmethod
    def source_name(self) -> str:
        """Name of the data source."""
        pass
