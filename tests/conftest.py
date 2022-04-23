import pytest
from flask_sqlalchemy import SQLAlchemy
from flask_login import FlaskLoginClient

from app import webapp


@pytest.fixture()
def app():
    app = webapp
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"  # in-memory test db
    )

    app.test_client_class = FlaskLoginClient

    # get the database object and create the tables inside the memory test-database
    from app import db
    db.init_app(app)
    db.create_all()
    yield app

    # Can add cleanup here


@pytest.fixture()
def db(app):
    from app import db
    yield db


@pytest.fixture()
def client(app):
    return app.test_client()
