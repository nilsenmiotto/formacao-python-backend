from datetime import datetime
from http import HTTPStatus

from src.controllers.post import _format_post, _format_posts
from src.messages import MESSAGE_POST_CREATED


def test_create_post(client, access_token, user_maria):
    # Given
    json_post = {
        "title": "Meu Post",
        "body": "Conteúdo do meu post",
        "created": datetime.now().isoformat(),
        "author_id": user_maria.id,
    }

    # When
    response = client.post(
        "/posts/", json=json_post, headers={"Authorization": f"Bearer {access_token}"}
    )

    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == MESSAGE_POST_CREATED


def test_list_post(client, access_token, post_maria):
    # Given
    post_maria

    # When
    response = client.get(
        "/posts/", headers={"Authorization": f"Bearer {access_token}"}
    )

    # Then
    assert response.status_code == HTTPStatus.OK


def test_get_post_success(client, access_token, post_maria):
    # Given

    # When
    response = client.get(
        f"/posts/{post_maria.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == _format_post(post_maria)


def test_get_post_fail(client, access_token):
    # Given
    post_id = 1000

    # When
    response = client.get(
        f"/posts/{post_id}", headers={"Authorization": f"Bearer {access_token}"}
    )

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_post_success(client, access_token, post_maria):
    # Given
    json_post = {
        "title": "Meu Post",
        "body": "alterando conteúdo do meu post",
        "created": datetime.now().isoformat(),
        "author_id": post_maria.author_id,
    }

    # When
    response = client.patch(
        f"/posts/{post_maria.id}",
        json=json_post,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json["body"] == json_post["body"]


def test_update_post_fail(client, access_token):
    # Given
    post_id = 1000
    json_post = {}

    # When
    response = client.patch(
        f"/posts/{post_id}",
        json=json_post,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_post_success(client, access_token, post_maria):
    # Given

    # When
    response = client.delete(
        f"/posts/{post_maria.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Then
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_post_fail(client, access_token):
    # Given
    post_id = 1000

    # When
    response = client.delete(
        f"/posts/{post_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
