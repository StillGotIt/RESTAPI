from pydantic import BaseModel


class BuildingSchema(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingQuerySchema(BaseModel):
    id: int | None
    latitude: float | None
    longitude: float | None
    radius_km: float | None

    def to_dict_without_none_values(self):
        return {
            key: value
            for key, value in {
                "id": self.id,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "radius_km": self.radius_km,
            }.items()
            if value is not None
        }
