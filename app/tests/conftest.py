import pytest

from api import create_app
from extensions import db
from config import SQLALCHEMY_DATABASE_URI
from models import Users, Classes, Picture
from sqlalchemy_utils import database_exists, drop_database, create_database


@pytest.fixture(scope="session")
def app():
    if database_exists(SQLALCHEMY_DATABASE_URI):
        drop_database(SQLALCHEMY_DATABASE_URI)
    create_database(SQLALCHEMY_DATABASE_URI)

    app = create_app()
    app.testing = True

    with app.app_context():
        db.session.execute('CREATE EXTENSION IF NOT EXISTS "zerobot_test"')
        db.session.commit()
        db.create_all()
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()
        drop_database(SQLALCHEMY_DATABASE_URI)


@pytest.fixture(scope='class')
def add_pictures(request):
    uuid = "cfa0a6b0-6a91-45b1-b68e-b01d0af3b43a"
    picture1 = Picture(id=1,
                       picture="pic_1",
                       uuid=uuid)
    picture2 = Picture(id=2,
                       picture="pic_2",
                       uuid=uuid)
    picture3 = Picture(id=3,
                       picture="pic_3",
                       uuid=uuid)
    picture4 = Picture(id=4,
                       picture="pic_4",
                       uuid=uuid)
    db.session.add(picture1)
    db.session.add(picture2)
    db.session.add(picture3)
    db.session.add(picture4)
    db.session.flush()

    request.cls.uuid = uuid
    return uuid


@pytest.fixture(scope='class')
def add_classes(request):
    uuid = "cfa0a6b0-6a91-45b1-b68e-b01d0af3b43a"
    classes1 = Classes(id=1,
                       choice="dog",
                       uuid=uuid)
    classes2 = Classes(id=2,
                       choice="cat",
                       uuid=uuid)
    classes3 = Classes(id=3,
                       choice="whale",
                       uuid=uuid)
    db.session.add(classes1)
    db.session.add(classes2)
    db.session.add(classes3)
    db.session.flush()

    request.cls.uuid = uuid
    return uuid


@pytest.fixture(scope='class')
def add_user(request):
    user = Users(id=1,
                 username="Zero_ABC",
                 password="Bot_123",
                 telegram_user="Zero_Bot")
    db.session.add(user)
    db.session.flush()
    request.cls.user = user
    return user
