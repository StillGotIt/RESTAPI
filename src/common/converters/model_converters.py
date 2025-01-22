from src.domain.schemas.activity import ActivitySchema
from src.domain.schemas.building import BuildingSchema
from src.domain.schemas.organization import (
    FullOutOrganizationSchema,
    OrganizationSchema,
)
from src.domain.schemas.phone import PhoneSchema
from src.infra.models.models import Organization


def convert_to_organization_entity(model: Organization) -> FullOutOrganizationSchema:
    return FullOutOrganizationSchema(
        organization=OrganizationSchema(name=model.name),
        phones=[PhoneSchema(number=phone.number) for phone in model.phones],
        building=BuildingSchema(
            address=model.building.address,
            longitude=model.building.longitude,
            latitude=model.building.latitude,
        ),
        activities=[
            ActivitySchema(name=activity.name) for activity in model.activities
        ],
    )


def convert_to_organization_entity_from_dict(
    model: Organization,
) -> FullOutOrganizationSchema:
    try:
        return FullOutOrganizationSchema(
            organization=OrganizationSchema(name=model.get("organization_name")),
            phones=[
                PhoneSchema(number=phone_number)
                for phone_number in model.get("phone_numbers")
            ],
            building=BuildingSchema(
                address=model.get(
                    "building_address",
                ),
                longitude=model.get(
                    "building_longitude",
                ),
                latitude=model.get(
                    "building_latitude",
                ),
            ),
            activities=[
                ActivitySchema(
                    name=model.get(
                        "activity_name",
                    )
                )
            ],
        )
    except ValueError as e:
        raise e


def convert_to_activity_entity(model: ActivitySchema) -> ActivitySchema:
    return ActivitySchema(name=model.name)
