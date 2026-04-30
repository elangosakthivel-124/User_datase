def test_weak_password():
    response = client.post("/register", json={
        "name": "Weak",
        "email": "weak@example.com",
        "age": 25,
        "password": "weak"
    })

    assert response.status_code == 422


def test_invalid_email():
    response = client.post("/register", json={
        "name": "Invalid",
        "email": "invalid-email",
        "age": 25,
        "password": "StrongPass1"
    })

    assert response.status_code == 422
