from datetime import datetime
from email.utils import format_datetime

import pytest

from src.app import create_app, bcrypt
from src.models import Role, User, Post, db


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

    password = "mudar123"
    user = User(
        username="john-doe",
        password=bcrypt.generate_password_hash(password),
        role_id=role.id,
    )
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login", json={"username": user.username, "password": password}
    )
    return response.json["access_token"]


@pytest.fixture()
def user_maria():
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    password = "mudar123"
    user = User(
        username="maria",
        password=bcrypt.generate_password_hash(password),
        role_id=role.id,
    )
    db.session.add(user)
    db.session.commit()

    # user_data = User(
    #    id=user.id,
    #    username=user.username,
    #    password=password,
    #    role_id=user.role_id,
    #    role=user.role,
    #    active=user.active,
    # )
    return user


@pytest.fixture()
def post_maria(user_maria):

    dt = datetime.now().isoformat()
    post = Post(
        title="Meu post",
        body="Conteudo",
        created=datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f"),
        author_id=user_maria.id,
    )
    db.session.add(post)
    db.session.commit()

    # post_data = Post(
    #    id=post.id,
    #    title=post.title,
    #    body=post.body,
    #    created=post.created,
    #    author_id=post.author_id,
    # )
    return post
