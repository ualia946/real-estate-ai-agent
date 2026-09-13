from abc import ABC, abstractmethod

from src.core.domain.entity.price_observation import PriceObservation
from src.core.domain.entity.property import Property
from src.core.domain.value_object.property_metadata import OperationType, PropertyType


class IPropertyRepositoryPort(ABC):
    """
    Port interface for persistent storage of properties.
    """

    @abstractmethod
    def save_property(self, property: Property) -> None:
        """
        Saves a newly extracted property into the database.
        """
        pass

    @abstractmethod
    def add_price_observation(self, observation: PriceObservation) -> None:
        """
        Appends a new price observation for a property (append-only history).
        """
        pass

    @abstractmethod
    def get_by_id(self, property_id: str) -> Property | None:
        """
        Retrieves a property by its unique identifier.
        """
        pass
    
    @abstractmethod
    def mark_as_inactive(self, property_id: str) -> None:
        """
        Marks a property as no longer available on the market, 
        instead of hard deleting it.
        """
        pass

    @abstractmethod
    def find_active_comparables(
        self,
        city: str,
        neighborhood: str,
        operation_type: OperationType,
        property_type: PropertyType,
    ) -> list[Property]:
        """
        Retrieves active historical properties in a specific area and of the same type
        to be used as a market baseline.
        """
        pass
