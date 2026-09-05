from dataclasses import dataclass


@dataclass(frozen=True)
class Amenities:
    has_terrace: bool
    has_parking_space: bool
    has_air_conditioning: bool
    is_furnished: bool
