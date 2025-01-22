from dataclasses import dataclass

from sqlalchemy.exc import SQLAlchemyError

from src.common.converters.model_converters import (
    convert_to_organization_entity,
    convert_to_organization_entity_from_dict,
)
from src.domain.schemas.activity import ActivityQuerySchema
from src.domain.schemas.organization import (
    OrganizationQuerySchema,
    FullOutOrganizationSchema,
)
from src.infra.db.db import AsyncPostgresClient
from src.infra.repos.organization_repo import OrganizationRepository


@dataclass(eq=False)
class OrganizationService:
    repository: OrganizationRepository
    async_client: AsyncPostgresClient

    async def get_organization_by_entity(
        self, organization_entity: OrganizationQuerySchema
    ) -> FullOutOrganizationSchema | None:
        async with self.async_client.create_session() as session:
            try:
                result = await self.repository.get_organization_by_entity(
                    session=session,
                    data=organization_entity.to_dict_without_none_values(),
                )
                if result:
                    return convert_to_organization_entity(result)
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    async def get_organizations_from_building_id(self, building_id: int):
        async with self.async_client.create_session() as session:
            try:
                results = await self.repository.get_organizations_from_building_id(
                    session=session, building_id=building_id
                )
                if results:
                    return [
                        convert_to_organization_entity(result) for result in results
                    ]
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    async def get_organizations_by_activity(
        self, activity_schema: ActivityQuerySchema
    ) -> list[FullOutOrganizationSchema] | None:
        async with self.async_client.create_session() as session:
            try:
                results = await self.repository.get_organizations_by_activity(
                    session=session, data=activity_schema.to_dict_without_parent()
                )
                if results:
                    return [
                        convert_to_organization_entity(result) for result in results
                    ]
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    async def get_organizations_in_radius(
        self, latitude: float, longitude: float, radius_km: float
    ) -> list[FullOutOrganizationSchema] | None:
        async with self.async_client.create_session() as session:
            try:
                results = await self.repository.get_organizations_in_radius(
                    session=session,
                    latitude=latitude,
                    longitude=longitude,
                    radius_km=radius_km,
                )
                if results:
                    return [
                        convert_to_organization_entity(result) for result in results
                    ]
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    async def get_organizations_by_activity_tree(
        self, activity_schema: ActivityQuerySchema
    ) -> list[FullOutOrganizationSchema] | None:
        async with self.async_client.create_session() as session:
            try:
                results = await self.repository.get_organizations_by_activity_tree(
                    session=session, data=activity_schema.to_dict_without_parent()
                )
                if results:
                    return [
                        convert_to_organization_entity_from_dict(result)
                        for result in results
                    ]
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
