from dataclasses import dataclass

from src.domain.entities.base import BaseEntity


@dataclass(eq=False)
class ActivityEntity(BaseEntity):
    name: str

    def to_dict(self):
        return {"name": self.name}
