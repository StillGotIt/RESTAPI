from fastapi import APIRouter, Depends, Query, HTTPException

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


def get_api_key(api_key: str = Query(..., description="API key required")):
    valid_api_keys = ["some_valid_api_key_213hj123hMEga_confidential"]

    if api_key not in valid_api_keys:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return api_key



@router.get("/organizations/", description="Returns organizations")
async def get(
    api_key: str = Depends(get_api_key),
    schema: OrganizationQuerySchema = Depends(get_organization_query_params),
) -> FullOutOrganizationSchema | None:
    service = OrganizationService(
        repository=OrganizationRepository(), async_client=AsyncPostgresClient()
    )
    result = await service.get_organization_by_entity(organization_entity=schema)
    if not result:
        return None
    return result


@router.get("/organizations/activities/", description="Returns organizations by activity they belong")
async def get(
        api_key: str = Depends(get_api_key),
        schema: ActivityQuerySchema = Depends(get_activity_query_params)):
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


@router.get("/organizations/buildings/", description="Returns organizations by building they belong")
async def get(
        api_key: str = Depends(get_api_key),
        schema: BuildingQuerySchema = Depends(get_building_query_params)):
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
