from dataclasses import dataclass

from src.core.domain.errors import InvalidCoordinatesError


@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not (-90.0 <= self.latitude <= 90.0):
            raise InvalidCoordinatesError(
                self.latitude, self.longitude, "Latitude must be between -90 and 90"
            )

        if not (-180.0 <= self.longitude <= 180.0):
            raise InvalidCoordinatesError(
                self.latitude, self.longitude, "Longitude must be between -180 and 180"
            )


@dataclass(frozen=True)
class Location:
    neighborhood: str
    city: str
    coordinates: Coordinates | None = None
