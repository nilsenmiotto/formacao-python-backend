import os

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .models.base import db

migrate = Migrate()
jwt = JWTManager()


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
