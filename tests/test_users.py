from fastapi import status


def test_create_user(client):

    response = client.post(
        "/users/",
        json={
            "email": "newuser@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["email"] == "newuser@test.com"
    assert "id" in data
    assert "created_at" in data


def test_duplicate_user(client, test_user):

    response = client.post(
        "/users/",
        json={
            "email": test_user["email"],
            "password": "password123"
        }
    )

    assert response.status_code == status.HTTP_409_CONFLICT

    assert response.json()["detail"] == \
        "An account with this email already exists"


def test_invalid_email(client):

    response = client.post(
        "/users/",
        json={
            "email": "invalid",
            "password": "password123"
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY