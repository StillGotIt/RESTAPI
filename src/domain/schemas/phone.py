from pydantic import BaseModel


class PhoneSchema(BaseModel):
    number: str
