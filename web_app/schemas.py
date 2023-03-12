from pydantic import BaseModel, Field
from pydantic.typing import Optional


class SoftwareBase(BaseModel):
    name: Optional[str]
    version: Optional[str]


class SoftwareCreate(SoftwareBase):
    pass


class Software(SoftwareBase):
    id: int

    class Config:
        orm_mode = True
