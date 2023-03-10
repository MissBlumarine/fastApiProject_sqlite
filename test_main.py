from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all_software():
    response = client.get("/versions/", headers={"X-Token": "'croldataerror'"})
    assert response.status_code == 200
    assert response.json() == [{"id": 2, "software": "sust", "version": "3.5"},
                               {"id": 3, "software": "crolend", "version": "1.4"}]


def test_create_software():
    response = client.post(
        "/version",
        json={"id": 1, "software": "rooti", "version": "2.5"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "software": "rooti",
        "version": "2.5"
    }


def test_create_software_existing():
    response = client.post(
        "/version",
        json={"id": 1, "software": "rooti", "version": "2.5"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Уже существует"}


