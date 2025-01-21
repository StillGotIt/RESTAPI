from dataclasses import dataclass

from src.domain.entities.base import BaseEntity


@dataclass(eq=False)
class PhoneEntity(BaseEntity):
    number: str

    def to_dict(self):
        return {"number": self.number}
