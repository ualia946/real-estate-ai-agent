from dataclasses import dataclass
from enum import Enum


class Orientation(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class BuildingDetails:
    floor: int
    has_elevator: bool
    is_exterior: bool
    orientation: Orientation
