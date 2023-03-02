from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
from fastapi import FastAPI

# строка подключения к БД
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_software.db"

# создаем движок
# в параметрах указываем сроку подключения и параметр connect_args, который
# позволяет в рамках одного запроса к БД использовать больше, чем один поток (для FastAPI)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# базовый класс
Base = declarative_base()


# модель, объекты которой будут записываться в БД
class Software(Base):
    __tablename__ = "software"

    id = Column(Integer, primary_key=True, index=True)
    software = Column(String)
    version = Column(String)


SessionLocal = sessionmaker(autoflush=False, bind=engine)
