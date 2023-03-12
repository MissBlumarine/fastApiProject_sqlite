import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists


from schemas import *
from crud import *
from database_config import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         db.begin()
#         yield db
#     finally:
#         db.rollback()
#         db.close()

def override_get_db():
    connection = engine.connect()
    transaction = connection.begin()

    db = Session(bind=connection)

    yield db

    db.close()
    transaction.rollback()
    connection.close()

app.dependency_overrides[get_db] = override_get_db()

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    # db = Session(db_engine)
    app.dependency_overrides[get_db] = lambda: db

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client_test(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture
def items(db):
    create_software(db, schemas.SoftwareCreate(name='lucy_1', version='1.1'))
    create_software(db, schemas.SoftwareCreate(name='lucy_2', version='1.2'))

