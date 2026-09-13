from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.core.domain.value_object import Money


@dataclass(frozen=True)
class PriceObservation:
    property_id: str
    price: Money
    observed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

