from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "api/v1/signup/",
        json={"username": "test", "password": "12345678"},
    )
    assert response.status_code == 200

def test_login():
    response = client.post(
        "api/v1/auth/",
        data={"username": "test", "password": "12345678"},
    )
    assert response.status_code == 200
    assert "access" in response.json()
    assert "refresh" in response.json()


def test_me():
    response = client.get(
        "api/v1/user/",
        headers={"Authorization": "Bearer wrong_token"},
    )
    assert response.status_code == 401


def test_me_with_token():
    response = client.post(
        "api/v1/auth/",
        data={"username": "test", "password": "12345678"},
    )
    token = response.json()["access"]
    response = client.get(
        "api/v1/user/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "test"


def test_create_task():
    response = client.post(
        "api/v1/auth/",
        data={"username": "test", "password": "12345678"},
    )
    token = response.json()["access"]
    response = client.post(
        "api/v1/task/",
        headers={"Authorization": f"Bearer {token}"},
        json={"ip": "127.0.0.1"},
    )
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_status():
    response = client.post(
        "api/v1/auth/",
        data={"username": "test", "password": "12345678"},
    )
    token = response.json()["access"]
    response = client.post(
        "api/v1/task/",
        headers={"Authorization": f"Bearer {token}"},
        json={"ip": "127.0.0.1"}
    )
    task_id = response.json()["id"]
    response = client.get(
        f"api/v1/status/{task_id}/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
