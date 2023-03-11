from pydantic import BaseModel, Field
from pydantic.typing import Optional


class SoftwareBase(BaseModel):
    software: Optional[str]
    version: Optional[str]


class SoftwareCreate(SoftwareBase):
    pass


class SoftwareOut(SoftwareBase):
    id: int


class SoftwareUpdate(SoftwareBase):
    id: int


class Software(SoftwareBase):
    id: Optional[int]

    class Config:
        orm_mode = True
