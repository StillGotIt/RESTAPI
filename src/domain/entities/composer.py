from dataclasses import dataclass

from src.domain.entities.activities import ActivityEntity
from src.domain.entities.base import BaseEntity
from src.domain.entities.buildings import BuildingEntity
from src.domain.entities.organizations import OrganizationEntity
from src.domain.entities.phones import PhoneEntity


@dataclass(eq=False)
class OrganizationComposerEntity(BaseEntity):
    activity_entities_list: list[ActivityEntity]
    organization_entity: OrganizationEntity
    building_entity: BuildingEntity
    phone_entity: PhoneEntity

    def to_dict(self):
        return {
            "organization": self.organization_entity.to_dict(),
            "activity": self.activity_entities_list,
            "building": self.building_entity.to_dict(),
            "phone": self.phone_entity.to_dict(),
        }
