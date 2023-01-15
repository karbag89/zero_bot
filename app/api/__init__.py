import logging

from flask import Flask
from models import  users, statistics, task, picture, classes
from extensions import config_extensions
from config import SQLALCHEMY_DATABASE_URI


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.url_map.strict_slashes = False
    app.logger.setLevel(logging.INFO)

    config_extensions(app)

    return app
