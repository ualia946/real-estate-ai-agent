from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.core.domain.value_object import (
    Amenities,
    BuildingDetails,
    Location,
    Money,
    PhysicalDimensions,
    ConservationState,
    OperationType,
    PropertyType,
)


@dataclass
class Property:
    id: str
    title: str
    description: str
    url: str
    price: Money
    location: Location
    dimensions: PhysicalDimensions
    building: BuildingDetails
    amenities: Amenities
    operation_type: OperationType
    property_type: PropertyType
    condition: ConservationState
    is_active: bool = True
    scraped_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def price_per_m2(self) -> float:
        return self.price.amount / self.dimensions.square_meters
