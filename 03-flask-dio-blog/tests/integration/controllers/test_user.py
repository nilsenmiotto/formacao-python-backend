from http import HTTPStatus

from src.controllers.user import _format_user, _format_users
from src.messages import MESSAGE_USER_CREATED
from src.models import User, db


def test_create_user(client, access_token):
    # Given
    json_user = {"username": "maria", "password": "minha senha", "role_id": 1}

    # When
    response = client.post(
        "/users/", json=json_user, headers={"Authorization": f"Bearer {access_token}"}
    )

    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == MESSAGE_USER_CREATED


def test_list_users(client, access_token):
    # Given

    # When
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {access_token}"}
    )

    # Then
    assert response.status_code == HTTPStatus.OK


def test_get_user_success(client, access_token, user_maria):
    # Given

    # When
    response = client.get(
        f"/users/{user_maria.id}", headers={"Authorization": f"Bearer {access_token}"}
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == _format_user(user_maria)


def test_get_user_fail(client, access_token):
    # Given
    user_id = 1000

    # When
    response = client.get(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {access_token}"}
    )

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user_success(client, access_token, user_maria):
    # Given
    json_user = {"username": "maria", "password": "minha senha", "role_id": 1}

    # When
    response = client.patch(
        f"/users/{user_maria.id}",
        json=json_user,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    user_alterado = db.get_or_404(User, user_maria.id)

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == _format_user(user_alterado)


def test_update_user_fail(client, access_token):
    # Given
    user_id = 1000
    json_user = {"username": "maria", "password": "minha senha", "role_id": 1}

    # When
    response = client.patch(
        f"/users/{user_id}",
        json=json_user,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_success(client, access_token, user_maria):
    # Given

    # When
    response = client.delete(
        f"/users/{user_maria.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Then
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_fail(client, access_token):
    # Given
    user_id = 1000

    # When
    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
