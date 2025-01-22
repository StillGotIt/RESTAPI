import asyncio

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities.activities import ActivityEntity
from src.domain.entities.buildings import BuildingEntity
from src.domain.entities.composer import OrganizationComposerEntity
from src.domain.entities.organizations import OrganizationEntity
from src.domain.entities.phones import PhoneEntity
from src.infra.db.db import AsyncPostgresClient
from src.infra.models.models import (
    Organization,
    Building,
    Phone,
    Activity,
    BaseSQLModel,
)


fake = Faker()

client_session = AsyncPostgresClient()


async def create_tables():
    async with client_session.engine.begin() as conn:
        await conn.run_sync(BaseSQLModel.metadata.create_all)


async def generate_data(entity: OrganizationComposerEntity):
    async with client_session.create_session() as session:
        try:
            organization = Organization(
                name=entity.organization_entity.name,
            )
            organization.building = Building(**entity.building_entity.to_dict())
            for phone_entity in entity.phones_entities_list:
                organization.phones.append(Phone(number=phone_entity.number))

            parent_activity = Activity(name=entity.activity_entities_list[0].name)
            child_activity = Activity(
                name=entity.activity_entities_list[-1].name, parent=[parent_activity]
            )
            organization.activities.append(child_activity)

            session.add(organization)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e


async def bulk_generate(organizations_number: int):
    tasks = []

    for _ in range(organizations_number):
        tasks.append(
            generate_data(
                OrganizationComposerEntity(
                    activity_entities_list=[
                        ActivityEntity(name=fake.job()),
                        ActivityEntity(name=fake.job()),
                    ],
                    organization_entity=OrganizationEntity(name=fake.name()),
                    building_entity=BuildingEntity(
                        address=fake.address(),
                        latitude=fake.latitude(),
                        longitude=fake.longitude(),
                    ),
                    phones_entities_list=[
                        PhoneEntity(number=fake.phone_number()),
                        PhoneEntity(number=fake.phone_number()),
                    ],
                )
            )
        )

    return await asyncio.gather(*tasks)


async def main():
    await create_tables()
    await bulk_generate(50)


if __name__ == "__main__":
    asyncio.run(main())
