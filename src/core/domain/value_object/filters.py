from dataclasses import dataclass

from ..errors import InvalidFilterError
from .money import Money


@dataclass(frozen=True)
class RealEstateFilters:
    city: str
    min_price: Money | None = None
    max_price: Money | None = None
    min_square_meters: float | None = None
    min_rooms: int | None = None
    needs_elevator: bool | None = None

    def __post_init__(self) -> None:
        if self.min_square_meters is not None and self.min_square_meters < 0:
            raise InvalidFilterError("Minimum square meters cannot be negative")

        if self.min_rooms is not None and self.min_rooms < 1:
            raise InvalidFilterError("Minimum rooms must be at least 1")

        if self.min_price is not None and self.max_price is not None:
            if self.min_price.currency != self.max_price.currency:
                raise InvalidFilterError(
                    "Currencies must match between min and max price"
                )
            if self.max_price.amount < self.min_price.amount:
                raise InvalidFilterError("Max price cannot be less than min price")
