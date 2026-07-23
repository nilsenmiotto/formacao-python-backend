from datetime import datetime

import pytest

from src.app import create_app, db
from src.models import Role, User, Post


@pytest.fixture()
def app():
    app = create_app(environment="Testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def access_token(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="john-doe", password="mudar123", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login", json={"username": user.username, "password": user.password}
    )
    return response.json["access_token"]


@pytest.fixture()
def user_maria():
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="maria", password="mudar123", role_id=role.id)
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def post_maria(user_maria):
    post = Post(
        title="Meu post",
        body="Conteudo",
        created=datetime.now(),
        author_id=user_maria.id,
    )
    db.session.add(post)
    db.session.commit()

    return post
