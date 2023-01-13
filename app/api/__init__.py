import logging

from flask import Flask
from models import  users, statistics, task, picture, classes
from extensions import config_extensions


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://zerobot:password@localhost:5432/zerobot"
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.url_map.strict_slashes = False
    app.logger.setLevel(logging.INFO)

    config_extensions(app)

    return app
