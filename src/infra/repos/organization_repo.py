from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.infra.models.models import Organization, organization_activity, Activity, Building
from geopy.distance import geodesic


@dataclass(eq=False)
class OrganizationRepository:
    model = Organization

    async def get_organization_by_id(self, session: AsyncSession, organization_id: int):
        query = (
            select(self.model)
            .where(self.model.id == organization_id)
            .options(
                selectinload(self.model.phones),
                selectinload(self.model.building),
                selectinload(self.model.activities)
            )
        )
        result = await session.execute(query)
        organization = result.scalars().first()
        return organization

    async def get_organizations_from_building_id(self, building_id: int, session: AsyncSession):
        query = (
            select(self.model)
            .where(self.model.building_id == building_id)
            .options(
                selectinload(self.model.phones),
                selectinload(self.model.building)
            )
        )
        result = await session.execute(query)
        organizations = result.scalars().all()
        return organizations

    async def get_organizations_by_activity(self, session: AsyncSession, activity_name: str):
        query = (
            select(self.model)
            .join(organization_activity, self.model.id == organization_activity.c.organization_id)
            .join(Activity, organization_activity.c.activity_id == Activity.id)
            .where(Activity.name == activity_name)
            .options(
                selectinload(self.model.phones),
                selectinload(self.model.building)
            )
        )
        result = await session.execute(query)
        organizations = result.scalars().all()
        return organizations

    async def get_organizations_in_radius(self, session: AsyncSession, latitude: float, longitude: float, radius_km: float):
        query = select(Building)
        result = await session.execute(query)
        buildings = result.scalars().all()

        target_point = (latitude, longitude)
        buildings_in_radius = [
            building for building in buildings
            if geodesic(target_point, (building.latitude, building.longitude)).km <= radius_km
        ]

        organizations = []
        for building in buildings_in_radius:
            query = (
                select(self.model)
                .where(self.model.building_id == building.id)
                .options(
                    selectinload(self.model.phones),
                    selectinload(self.model.building)
                )
            )
            result = await session.execute(query)
            organizations.extend(result.scalars().all())

        return organizations

    async def get_organizations_by_activity_tree(self, session: AsyncSession, activity_name: str):
        query = select(Activity).where(Activity.name == activity_name)
        result = await session.execute(query)
        root_activity = result.scalars().first()

        if not root_activity:
            return []

        def get_all_child_activities(activity):
            activities = [activity]
            for child in activity.children:
                activities.extend(get_all_child_activities(child))
            return activities

        all_activities = get_all_child_activities(root_activity)

        query = (
            select(self.model)
            .join(organization_activity, self.model.id == organization_activity.c.organization_id)
            .where(organization_activity.c.activity_id.in_([a.id for a in all_activities]))
            .options(
                selectinload(self.model.phones),
                selectinload(self.model.building)
            )
        )
        result = await session.execute(query)
        organizations = result.scalars().all()
        return organizations

    async def search_organizations_by_name(self, session: AsyncSession, name: str):
        query = (
            select(self.model)
            .where(self.model.name.ilike(f"%{name}%"))
            .options(
                selectinload(self.model.phones),
                selectinload(self.model.building)
            )
        )
        result = await session.execute(query)
        organizations = result.scalars().all()
        return organizations

    async def get_activities_with_depth_limit(self, session: AsyncSession, max_depth: int = 3):
        def get_activities_with_depth(activity, current_depth):
            if current_depth > max_depth:
                return []
            activities = [activity]
            for child in activity.children:
                activities.extend(get_activities_with_depth(child, current_depth + 1))
            return activities

        query = select(Activity).where(Activity.parent_id == None)
        result = await session.execute(query)
        root_activities = result.scalars().all()

        all_activities = []
        for root in root_activities:
            all_activities.extend(get_activities_with_depth(root, 1))

        return all_activities
