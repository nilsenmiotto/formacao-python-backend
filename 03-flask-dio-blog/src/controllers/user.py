from http import HTTPStatus

from flask import Blueprint, request
from sqlalchemy import inspect

from app import User, db

app = Blueprint("user", __name__, url_prefix="/users")


def _format_user(user):
    return {"id": user.id, "username": user.username}


def _format_users(users):
    return [{"id": user.id, "username": user.username} for user in users]


def _create_user():

    data = request.get_json()
    user = User(username=data["username"])
    db.session.add(user)
    db.session.commit()
    return {"message": "User created"}, HTTPStatus.CREATED


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return _format_users(users)


@app.route("/", methods=["GET", "POST"])
def handle_users():
    if request.method == "GET":
        return _list_users()
    elif request.method == "POST":
        return _create_user()


@app.route("/<int:id>", methods=["GET"])
def get_user(id):
    user = db.get_or_404(User, id)
    return _format_user(user)


@app.route("/<int:id>", methods=["PATCH"])
def update_user(id):
    user = db.get_or_404(User, id)
    data = request.json

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])

    db.session.commit()
    return _format_user(user)


@app.route("/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
