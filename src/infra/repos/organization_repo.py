from dataclasses import dataclass
from typing import Any

from sqlalchemy import select, and_, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, aliased

from src.infra.models.models import (
    Organization,
    organization_activity,
    Activity,
    Building,
)
from geopy.distance import geodesic


@dataclass(eq=False)
class OrganizationRepository:
    model = Organization

    async def get_organization_by_entity(
        self, session: AsyncSession, data: dict[str, Any]
    ) -> Organization:
        query = (
            select(self.model)
            .filter_by(**data)
            .options(
                selectinload(self.model.phones),
                selectinload(self.model.building),
                selectinload(self.model.activities),
            )
        )
        result = await session.execute(query)
        organization = result.scalars().first()
        return organization

    async def get_organizations_from_building_id(
        self, building_id: int, session: AsyncSession
    ) -> [Organization | None]:
        query = (
            select(self.model)
            .where(self.model.building_id == building_id)
            .options(selectinload(self.model.phones), selectinload(self.model.building))
        )
        result = await session.execute(query)
        organizations = result.scalars().all()
        return organizations

    async def get_organizations_by_activity(
        self, session: AsyncSession, data: dict[str, Any]
    ) -> [Organization | None]:
        query = (
            select(self.model)
            .join(
                organization_activity,
                self.model.id == organization_activity.c.organization_id,
            )
            .join(Activity, organization_activity.c.activity_id == Activity.id)
            .filter_by(**data)
            .options(selectinload(self.model.phones), selectinload(self.model.building))
        )
        result = await session.execute(query)
        organizations = result.scalars().all()

        return organizations

    async def get_organizations_in_radius(
        self, session: AsyncSession, latitude: float, longitude: float, radius_km: float
    ) -> list[Organization | None]:
        delta_lat = radius_km / 111.32
        delta_lon = radius_km / (111.32 * abs(latitude))

        min_lat = latitude - delta_lat
        max_lat = latitude + delta_lat
        min_lon = longitude - delta_lon
        max_lon = longitude + delta_lon

        buildings_query = select(Building).where(
            and_(
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lon, max_lon),
            )
        )

        result = await session.execute(buildings_query)
        buildings_in_bbox = result.scalars().all()
        target_point = (latitude, longitude)
        buildings_in_radius = [
            building
            for building in buildings_in_bbox
            if geodesic(target_point, (building.latitude, building.longitude)).km
            <= radius_km
        ]

        organizations = []
        for building in buildings_in_radius:
            query = (
                select(self.model)
                .where(self.model.building_id == building.id)
                .options(
                    selectinload(self.model.phones), selectinload(self.model.building)
                )
            )
            result = await session.execute(query)
            organizations.extend(result.scalars().all())

        return organizations

    @staticmethod
    async def get_organizations_by_activity_tree(
        session: AsyncSession,
        data: dict[str, Any],
        max_depth: int = 3,
    ) -> [Organization | None]:
        query = text(
            """
            WITH RECURSIVE activity_tree AS (
                SELECT
                    id,
                    name,
                    parent_id,
                    1 AS depth
                FROM
                    activities
                UNION ALL

                SELECT
                    a.id,
                    a.name,
                    a.parent_id,
                    at.depth + 1 AS depth
                FROM
                    activities a
                INNER JOIN
                    activity_tree at ON a.parent_id = at.id
                WHERE
                    at.depth < :max_depth
            )
            SELECT DISTINCT
                o.id AS organization_id,
                o.name AS organization_name,
                b.id AS building_id,
                b.address AS building_address,
                b.latitude AS building_latitude,
                b.longitude AS building_longitude,
                array_agg(p.number) AS phone_numbers,
                at.id AS activity_id,
                at.name AS activity_name
            FROM
                organizations o
            INNER JOIN
                buildings b ON o.building_id = b.id
            LEFT JOIN
                phones p ON o.id = p.organization_id
            INNER JOIN
                organization_activity oa ON o.id = oa.organization_id
            INNER JOIN
                activity_tree at ON oa.activity_id = at.id
            GROUP BY
                o.id, o.name, b.id, b.address, b.latitude, b.longitude, at.id, at.name;
        """
        )
        # Параметры запроса
        params = {
            "activity_name": data.get("name", None),
            "activity_id": data.get("id", None),
            "max_depth": max_depth,
        }

        result = await session.execute(query, params)
        return result.mappings().fetchall()

    @staticmethod
    async def get_activities_with_depth_limit(
        session: AsyncSession, max_depth: int = 3
    ) -> [Organization | None]:
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

    @staticmethod
    async def get_all_children(session: AsyncSession, parent_id: int):
        cte = select(Activity).where(Activity.id == parent_id).cte(recursive=True)

        child_alias = aliased(Activity, name="child")

        cte = cte.union_all(
            select(child_alias).where(child_alias.parent_id == cte.c.id)
        )

        result = await session.execute(
            select(Activity).join(cte, Activity.id == cte.c.id)
        )
        children = result.scalars().all()
        return children
