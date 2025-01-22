from fastapi import APIRouter, Depends

from src.common.converters.query_converters import (
    get_organization_query_params,
    get_activity_query_params,
    get_building_query_params,
)
from src.domain.schemas.activity import ActivityQuerySchema
from src.domain.schemas.building import BuildingQuerySchema
from src.domain.schemas.organization import (
    OrganizationQuerySchema,
    FullOutOrganizationSchema,
)
from src.infra.db.db import AsyncPostgresClient
from src.infra.repos.organization_repo import OrganizationRepository
from src.logic.repo_services.organization_service import OrganizationService

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/organizations/")
async def get(
    schema: OrganizationQuerySchema = Depends(get_organization_query_params),
) -> FullOutOrganizationSchema | None:
    service = OrganizationService(
        repository=OrganizationRepository(), async_client=AsyncPostgresClient()
    )
    result = await service.get_organization_by_entity(organization_entity=schema)
    if not result:
        return None
    return result


@router.get("/organizations/activities/")
async def get(schema: ActivityQuerySchema = Depends(get_activity_query_params)):
    service = OrganizationService(
        repository=OrganizationRepository(), async_client=AsyncPostgresClient()
    )
    if schema.is_parent:
        result = await service.get_organizations_by_activity_tree(
            activity_schema=schema
        )
        return result
    result = await service.get_organizations_by_activity(activity_schema=schema)
    if not result:
        return None
    return result


@router.get("/organizations/buildings/")
async def get(schema: BuildingQuerySchema = Depends(get_building_query_params)):
    service = OrganizationService(
        repository=OrganizationRepository(), async_client=AsyncPostgresClient()
    )
    if schema.id:
        result = await service.get_organizations_from_building_id(building_id=schema.id)
        return result
    result = await service.get_organizations_in_radius(
        latitude=schema.latitude, longitude=schema.longitude, radius_km=schema.radius_km
    )
    if not result:
        return None
    return result
