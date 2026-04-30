import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_register_success():
    response = client.post("/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "age": 25,
        "password": "StrongPass1"
    })

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


def test_register_duplicate_email():
    client.post("/register", json={
        "name": "Test User",
        "email": "dup@example.com",
        "age": 25,
        "password": "StrongPass1"
    })

    response = client.post("/register", json={
        "name": "Test User",
        "email": "dup@example.com",
        "age": 25,
        "password": "StrongPass1"
    })

    assert response.status_code == 400


def test_login_success():
    client.post("/register", json={
        "name": "Login User",
        "email": "login@example.com",
        "age": 25,
        "password": "StrongPass1"
    })

    response = client.post("/login", json={
        "email": "login@example.com",
        "password": "StrongPass1"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_password():
    response = client.post("/login", json={
        "email": "login@example.com",
        "password": "WrongPass"
    })

    assert response.status_code == 401


def test_protected_route_requires_auth():
    response = client.get("/me")
    assert response.status_code == 401


def test_protected_route_with_token():
    register = client.post("/register", json={
        "name": "Protected User",
        "email": "protected@example.com",
        "age": 25,
        "password": "StrongPass1"
    })

    login = client.post("/login", json={
        "email": "protected@example.com",
        "password": "StrongPass1"
    })

    token = login.json()["access_token"]

    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
