from enum import Enum


class OperationType(Enum):
    SALE = "sale"
    RENT = "rent"


class ConservationState(Enum):
    RENOVATED = "renovated"
    GOOD = "good"
    NEEDS_RENOVATION = "needs_renovation"
    UNKNOWN = "unknown"


class PropertyType(Enum):
    FLAT = "flat"  # Piso
    HOUSE = "house"  # Chalet
    PENTHOUSE = "penthouse"  # Ático
    GROUND_FLOOR = "ground_floor"  # Bajo
    DUPLEX = "duplex"
    UNKNOWN = "unknown"

