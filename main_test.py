import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///.test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        db.begin()
        yield db
    finally:
        db.rollback()
        db.close()


# @pytest.fixture()
# def test_db():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_software():
    response = client.post(
        "/version",
        json={"id": 0, "software": "licy", "version": "4.5"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["version"] == '4.5'
    assert data["software"] == 'licy'
    assert 'id' in data
    id = data['id']


def test_create_software_exists():
    response = client.post(
        "/version",
        json={"id": 0, "software": "licy", "version": "4.5"}
    )
    assert response.status_code == 400, response.text


def test_get_all_software():
    response = client.get(
        "/versions"
    )
    assert response.status_code == 200
    data = response.json()
    assert data == [{"id": 0, "software": "licy", "version": "4.5"}]


# def test_get_software_by_id():
#     id = 0
#     response = client.get(f"/versions/{id}")
#     # assert response.status_code == 200
#     assert response.json() == {"id": 0, "software": "licy", "version": "4.5"}
#     assert response.json()["id"] == 0
#     assert response.json()['software'] == 'licy'
#     assert response.json()['version'] == '4.5'


# def test_get_software_by_id_none():
#     response = client.get(
#         f"/versions/{id}"
#     )
#     assert response.status_code == 400
