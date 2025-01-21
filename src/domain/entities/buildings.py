from dataclasses import dataclass
from decimal import Decimal

from src.domain.entities.base import BaseEntity


@dataclass(eq=False)
class BuildingEntity(BaseEntity):
    address: str
    latitude: Decimal
    longitude: Decimal

    def to_dict(self):
        return {
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
