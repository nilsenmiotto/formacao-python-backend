import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .models.base import db

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(environment=os.getenv("ENVIRONMENT")):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{environment.capitalize()}Config")

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

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
    bcrypt.init_app(app)

    return app
