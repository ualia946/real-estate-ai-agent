from abc import ABC, abstractmethod

from src.core.domain.entity.property import Property


class IExtractorPort(ABC):
    """
    Port interface for information extraction operations.
    This defines the contract for adapting unstructured text into Domain Entities.
    """

    @abstractmethod
    def extract_property(self, raw_text: str, url: str) -> Property:
        """
        Parses raw text (usually via AI/LLMs) and constructs a valid Property entity.

        Args:
            raw_text: The unstructured text or HTML scraped from the property page.
            url: The original URL of the property, needed to construct the Entity.

        Returns:
            A fully hydrated Property domain entity.
        """
        pass
