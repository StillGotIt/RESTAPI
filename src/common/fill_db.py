import asyncio

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError
from src.domain.entities.activities import ActivityEntity
from src.domain.entities.buildings import BuildingEntity
from src.domain.entities.composer import OrganizationComposerEntity
from src.domain.entities.organizations import OrganizationEntity
from src.domain.entities.phones import PhoneEntity
from src.infra.db.db import AsyncPostgresClient
from src.infra.models.models import Organization, Building, Phone, Activity, BaseSQLModel


fake = Faker()

client_session = AsyncPostgresClient()


async def create_tables():
    async with client_session.engine.begin() as conn:
        await conn.run_sync(BaseSQLModel.metadata.create_all)


async def bulk_generate(organizations_number: int):
    tasks = []

    for _ in range(organizations_number):
        tasks.append(generate_data(OrganizationComposerEntity(
            activity_entities_list=[ActivityEntity(name=fake.job()), ActivityEntity(name=fake.job())],
            organization_entity=OrganizationEntity(name=fake.name()),
            building_entity=BuildingEntity(address=fake.address(),
                                           latitude=fake.latitude(),
                                           longitude=fake.longitude()),
            phone_entity=PhoneEntity(number=fake.phone_number()), )))

    return await asyncio.gather(*tasks)


async def generate_data(entity: OrganizationComposerEntity):
    async with client_session.create_session() as session:
        try:
            organization = Organization(
                name=entity.organization_entity.name,
            )
            organization.building = Building(**entity.building_entity.to_dict())
            organization.phones.append(Phone(number=entity.phone_entity.number))

            for activity in entity.activity_entities_list:
                organization.activities.append(Activity(**activity.to_dict()))

            session.add(organization)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e


async def main():
    await bulk_generate(100)
    print("Данные успешно сгенерированы!")


if __name__ == "__main__":
    print(asyncio.run(main()))
