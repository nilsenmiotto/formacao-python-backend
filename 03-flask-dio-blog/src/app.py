import os
from datetime import datetime
import click
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import func
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()


class Role(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"Role(id={self.id!r}, name={self.name!r})"


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("role.id"), nullable=True)
    role: Mapped["Role"] = relationship(back_populates="user")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, active={self.active})"


class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(80), nullable=False)
    body: Mapped[str] = mapped_column(String(300), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    def __repr__(self):
        return (
            f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"
        )


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database.")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///dio-blog.sqlite",
        JWT_SECRET_KEY="Kfa8xiKMec707RNJGMzDWJIDxadurTTh1iiWP7tXUZA",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # register the database commands
    app.cli.add_command(init_db_command)

    # register the blueprints
    from .controllers import user
    from .controllers import post
    from .controllers import auth

    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(auth.app)

    # initialize the app with the extension
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    return app
