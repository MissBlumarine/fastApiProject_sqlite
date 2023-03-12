from crud import *
from main import app
from test_database_config import *
from fastapi.testclient import TestClient
from fastapi import status
from models import *


# Base.metadata.create_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_software(client_test):
    response = client.post(
        "/version",
        json={"name": "sugar", "version": "4.5"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["version"] == '4.5'
    assert data["name"] == 'sugar'
    assert 'id' in data


def test_create_software_exists(items, client_test):
    response = client.post(
        "/version",
        json={"name": "lucy_1", "version": "1.1"}
    )
    assert response.status_code == 400, response.text


def test_get_all_software(items, client_test):
    response = client.get(
        "/versions"
    )
    assert response.status_code == 200
    data = response.json()
    assert data == [
        {"id": 1, "name": "lucy_1", "version": "1.1"},
        {"id": 2, "name": "lucy_2", "version": "1.2"}
        ]


def test_get_software_by_id(items, client_test):
    response = client.get(f"/versions/1/")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "lucy_1", "version": "1.1"}


def test_get_software_by_id_none(items, client_test):
    response = client.get(f"/versions/3/")
    assert response.status_code == 404


def test_update_software_by_id(items, client_test):
    response = client.put(f"/version/1?name=i-lucy&version=1.3")
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == 'i-lucy'
    assert data["version"] == '1.3'


def test_update_software_by_id_none(items, client_test):
    response = client.put(f"/version/3?name=i-lucy&version=2.5")
    assert response.status_code == 404


# def test_update_software_by_id_patch(items, client_test):
#     # response = client.patch(f"/version/{id}", json={"id": 1, "version": "5.5"})
#     response = client.patch(f"/version/1", json={"id": 1, "name": "lucy_1", "version": "5.5"})
#     # response = client.patch(f"/version/1?name=i-lucy&version=5.5")
#
#     data = response.json()
#     print(response.headers)
#     assert "allow" in response.headers, response.headers
#     assert response.status_code == 200
#
#
#     assert data["name"] == 'lucy_1'
#     assert data["version"] == '5.5'
# #
#
# def test_update_software_by_id_patch_none(items, client_test):
#     response = client.patch(f"/version/3", json={"version": "5.5"})
#     assert response.status_code == 404


def test_delete_item_by_id(items, client_test):
    response = client.delete(f"/version/1")
    assert response.status_code == 200


def test_delete_item_by_id_none(items, client_test):
    response = client.delete(f"/version/3")
    assert response.status_code == 404
