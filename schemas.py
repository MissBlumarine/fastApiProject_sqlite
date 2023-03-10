from pydantic import BaseModel, Field


class SoftwareBase(BaseModel):
    software: str
    version: str


class SoftwareOut(SoftwareBase):
    id: int


class SoftwareCreate(SoftwareBase):
    id: int


class SoftwareUpdate(SoftwareBase):
    id: int


class Software(SoftwareBase):
    id: int

    #
    class Config:
        orm_mode = True
