from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.domain.value_object.filters import RealEstateFilters


@dataclass(frozen=True)
class BasicListing:
    """DTO representing a lightweight search result before full extraction."""

    url: str
    price: float
    square_meters: float


class IScraperPort(ABC):
    """
    Port interface for web scraping operations.
    This defines the contract that any web scraper adapter must implement.
    """

    @abstractmethod
    def search_properties(self, filters: RealEstateFilters) -> list[BasicListing]:
        """
        Searches a real estate portal using the provided business filters.

        Args:
            filters: A RealEstateFilters value object containing the search criteria.

        Returns:
            A list of BasicListing DTOs with minimal info for mathematical filtering.
        """
        pass

    @abstractmethod
    def get_property_details(self, url: str) -> str:
        """
        Fetches the complete, raw content of a specific property listing page.

        Args:
            url: The direct URL to the property listing.

        Returns:
            A string containing the raw text or markdown of the page,
            ready for AI analysis.
        """
        pass
