from sqlalchemy import Column, String, Integer
from database_config import Base


# модель, объекты которой будут записываться в БД
class Software(Base):
    __tablename__ = "software"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    version = Column(String)
    #
    # class Config:
    #     orm_mode = True
