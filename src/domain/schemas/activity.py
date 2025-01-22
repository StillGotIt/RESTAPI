from pydantic import BaseModel


class ActivitySchema(BaseModel):
    name: str | None


class ActivityQuerySchema(BaseModel):
    name: str | None
    is_parent: bool | None
    id: int | None

    def to_dict_without_none_values(self):
        return {
            key: value
            for key, value in {
                "name": self.name,
                "id": self.id,
                "is_parent": self.is_parent,
            }.items()
            if value is not None
        }

    def to_dict_without_parent(self):
        return {
            key: value
            for key, value in {
                "name": self.name,
                "id": self.id,
            }.items()
            if value is not None
        }
