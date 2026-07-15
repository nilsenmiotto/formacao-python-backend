from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect

from ..app import Post, db

app = Blueprint("post", __name__, url_prefix="/posts")


def _format_post(post):
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created,
        "author_id": post.author_id,
    }


def _format_posts(posts):
    return [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "created": post.created,
            "author_id": post.author_id,
        }
        for post in posts
    ]


def _create_post():
    data = request.get_json()
    print(data)
    post = Post(
        title=data["title"],
        body=data["body"],
        created=datetime.strptime(data["created"], "%Y-%m-%d %H:%M:%S"),
        author_id=data["author_id"],
    )
    db.session.add(post)
    db.session.commit()
    return {"Message": "Post created"}, HTTPStatus.CREATED


def _list_post():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return _format_posts(posts)


@app.route("/", methods=["GET", "POST"])
@jwt_required()
def handle_posts():
    if request.method == "GET":
        return _list_post()
    elif request.method == "POST":
        return _create_post()


@app.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_post(id):
    post = db.get_or_404(Post, id)
    return _format_post(post)


@app.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_post(id):
    post = db.get_or_404(Post, id)
    data = request.get_json()

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            if column.key == "created":
                setattr(
                    post,
                    column.key,
                    datetime.strptime(data[column.key], "%Y-%m-%d %H:%M:%S"),
                )
            else:
                setattr(post, column.key, data[column.key])

    db.session.commit()
    return _format_post(post)


@app.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_post(id):
    post = db.get_or_404(Post, id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
