import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
# from main import app, get_db
from main import *

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
        json={"software": "licy", "version": "4.5"}
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
        json={"software": "licy", "version": "4.5"}
    )
    assert response.status_code == 400, response.text


def test_get_all_software():
    response = client.get(
        "/versions"
    )
    assert response.status_code == 200
    data = response.json()
    assert data == [{"id": 1, "software": "licy", "version": "4.5"}]


def test_get_software_by_id():
    response = client.get(f"/versions/1/")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "software": "licy", "version": "4.5"}


def test_get_software_by_id_none():
    response = client.get(f"/versions/2/")
    assert response.status_code == 404


def test_update_software_by_id():
    response = client.put("/version/1", json={"id": 1, "software": "i_licy", "version": "2.5"})
    assert response.status_code == 200
