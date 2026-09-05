from abc import ABC, abstractmethod

from src.core.domain.entity.property import Property


class IPropertyRepositoryPort(ABC):
    """
    Port interface for persistent storage of properties.
    """

    @abstractmethod
    def save(self, property: Property) -> None:
        """
        Saves a newly extracted property into the database/storage.
        """
        pass

    @abstractmethod
    def get_by_id(self, property_id: str) -> Property | None:
        """
        Retrieves a property by its unique identifier.
        """
        pass

    @abstractmethod
    def find_comparables(self, city: str, neighborhood: str) -> list[Property]:
        """
        Retrieves historical properties in a specific area to be used as a market
        baseline.
        """
        pass
