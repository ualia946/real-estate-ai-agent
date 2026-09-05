from dataclasses import dataclass

from src.core.domain.errors import InvalidDimensionError


@dataclass(frozen=True)
class PhysicalDimensions:
    square_meters: float
    rooms: int
    bathrooms: int

    def __post_init__(self) -> None:
        if self.square_meters < 0:
            raise InvalidDimensionError("square_meters", self.square_meters)

        if self.rooms < 0:
            raise InvalidDimensionError("rooms", self.rooms)

        if self.bathrooms < 0:
            raise InvalidDimensionError("bathrooms", self.bathrooms)
