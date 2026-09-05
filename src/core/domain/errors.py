class DomainError(Exception):
    """Base exception for any errors in domain."""

    pass


class NegativePriceError(DomainError):
    def __init__(self, amount: float):
        super().__init__(f"Invalid price: it can not be negative (Recivied: {amount})")


class InvalidDimensionError(DomainError):
    def __init__(self, dimension_name: str, value: float):
        super().__init__(
            f"Invalid dimension for '{dimension_name}': "
            f"cannot be negative (Received: {value})"
        )


class UnsupportedCurrencyError(DomainError):
    def __init__(self, currency: str):
        super().__init__(f"Currency not supported by the system: {currency}")


class InvalidCoordinatesError(DomainError):
    def __init__(self, lat: float, lon: float, reason: str):
        super().__init__(f"Invalid coordinates ({lat}, {lon}): {reason}")


class InvalidFilterError(DomainError):
    def __init__(self, reason: str):
        super().__init__(f"Invalid search filter: {reason}")
