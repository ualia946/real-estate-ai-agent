from dataclasses import dataclass

from src.core.domain.value_object import (
    Amenities,
    BuildingDetails,
    Location,
    Money,
    PhysicalDimensions,
)


@dataclass
class Property:
    id: str
    title: str
    url: str
    price: Money
    location: Location
    dimensions: PhysicalDimensions
    building: BuildingDetails
    amenities: Amenities

    @property
    def price_per_m2(self) -> float:
        return self.price.amount / self.dimensions.square_meters
