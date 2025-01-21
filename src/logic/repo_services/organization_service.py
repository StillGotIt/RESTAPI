from dataclasses import dataclass

from sqlalchemy.exc import SQLAlchemyError

from src.infra.db.db import AsyncPostgresClient
from src.infra.repos.organization_repo import OrganizationRepository


@dataclass(eq=False)
class OrganizationService:
    repository: OrganizationRepository
    async_client: AsyncPostgresClient

    async def get_organization_by_id(self, organization_id: int):
        async with self.async_client.create_session() as session:
            try:
                result = await self.repository.get_organization_by_id(session=session, organization_id=organization_id)
                await session.commit()
                return result
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    async def get_organizations_from_building_id(self, building_id: int):
        async with self.async_client.create_session() as session:
            try:
                result = await self.repository.get_organizations_from_building_id(session=session,
                                                                                  building_id=building_id)
                await session.commit()
                return result
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    async def get_organizations_by_activity(self, activity_name: str):
        async with self.async_client.create_session() as session:
            try:
                result = await self.repository.get_organizations_by_activity(session=session,
                                                                             activity_name=activity_name)
                await session.commit()
                return result
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    async def get_organizations_in_radius(self, latitude: float, longitude: float, radius_km: float):
        async with self.async_client.create_session() as session:
            try:
                result = await self.repository.get_organizations_in_radius(session=session, latitude=latitude,
                                                                           longitude=longitude,
                                                                           radius_km=radius_km, )
                await session.commit()
                return result
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    async def get_organizations_by_activity_tree(self, activity_name: str):
        async with self.async_client.create_session() as session:
            try:
                result = await self.repository.get_organizations_by_activity_tree(session=session,
                                                                                  activity_name=activity_name)
                await session.commit()
                return result
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    async def search_organizations_by_name(self, name: str):
        async with self.async_client.create_session() as session:
            try:
                result = await self.repository.search_organizations_by_name(session=session, name=name)
                await session.commit()
                return result
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    async def get_activities_with_depth_limit(self, max_depth: int = 3):
        async with self.async_client.create_session() as session:
            try:
                result = await self.repository.get_activities_with_depth_limit(session=session)
                await session.commit()
                return result
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
