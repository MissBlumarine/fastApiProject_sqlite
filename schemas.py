from pydantic import BaseModel


class SoftwareBase(BaseModel):
    software: str
    version: str


class SoftwareCreate(SoftwareBase):
    pass


class Sofware(SoftwareBase):
    id: int

    class Config:
        orm_mode = True
