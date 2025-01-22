from fastapi import Query

from src.domain.schemas.activity import ActivityQuerySchema
from src.domain.schemas.building import BuildingQuerySchema
from src.domain.schemas.organization import OrganizationQuerySchema


def get_organization_query_params(
    name: str | None = Query(None, example="111", description="Organization name"),
    id: int | None = Query(None, example="Microsoft", description="Organization id"),
) -> OrganizationQuerySchema:
    return OrganizationQuerySchema(name=name, id=id)


def get_building_query_params(
    id: int | None = Query(default=None, description="Building id"),
    longitude: float | None = Query(default=None, description="longitude"),
    latitude: float | None = Query(default=None, description="latitude"),
    radius_km: float | None = Query(default=1, description="Radius zone in km"),
) -> BuildingQuerySchema:
    return BuildingQuerySchema(
        id=id,
        longitude=longitude,
        latitude=latitude,
        radius_km=radius_km,
    )


def get_activity_query_params(
    id: int | None = Query(None, example="Cleaning", description="Activity id"),
    is_parent: bool
    | None = Query(False, example=False, description="Is it parent activity"),
    name: str | None = Query(default=None, description="activity name"),
) -> ActivityQuerySchema:
    return ActivityQuerySchema(name=name, id=id, is_parent=is_parent)
