from http import HTTPStatus
from flask_jwt_extended import decode_token


def test_auth_success(client, user_maria):
    # Given
    json_login = {"username": user_maria.username, "password": "mudar123"}

    # When
    response = client.post("/auth/login", json=json_login)

    # Then
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json

    access_token = response.json["access_token"]
    assert isinstance(access_token, str)
    assert access_token != ""

    decoded = decode_token(access_token)
    assert decoded["sub"] == str(user_maria.id)
    assert decoded["type"] == "access"


def test_auth_fail(client):
    # Given
    json_login = {"username": "fulano", "password": "minha senha"}

    # When
    response = client.post("/auth/login", json=json_login)

    # Then
    assert response.status_code == HTTPStatus.UNAUTHORIZED
