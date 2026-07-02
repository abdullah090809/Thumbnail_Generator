from fastapi import status


def test_login_success(client, test_user):

    response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):

    response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": "wrongpassword"
        }
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert response.json()["detail"] == "Invalid credentials"


def test_login_wrong_email(client):

    response = client.post(
        "/auth/login",
        data={
            "username": "fake@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert response.json()["detail"] == "Invalid credentials"