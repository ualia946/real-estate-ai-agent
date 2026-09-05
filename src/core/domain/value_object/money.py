from dataclasses import dataclass

from src.core.domain.errors import NegativePriceError, UnsupportedCurrencyError


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "EUR"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise NegativePriceError(self.amount)

        if self.currency not in ["EUR", "USD"]:
            raise UnsupportedCurrencyError(self.currency)
