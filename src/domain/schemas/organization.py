from pydantic import BaseModel

from src.domain.schemas.activity import ActivitySchema
from src.domain.schemas.building import BuildingSchema
from src.domain.schemas.phone import PhoneSchema


class OrganizationSchema(BaseModel):
    name: str


class OrganizationQuerySchema(BaseModel):
    id: int | None
    name: str | None

    def to_dict_without_none_values(self):
        return {
            key: value
            for key, value in {
                "id": self.id,
                "name": self.name,
            }.items()
            if value is not None
        }


class FullOutOrganizationSchema(BaseModel):
    organization: OrganizationSchema
    phones: list[PhoneSchema]
    building: BuildingSchema
    activities: list[ActivitySchema]
