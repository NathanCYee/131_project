import pytest
from flask_login import FlaskLoginClient
from app.models import *

from app import webapp


@pytest.fixture()
def app():
    app = webapp
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",  # in-memory test db
        WTF_CSRF_ENABLED=False  # disable CSRF for easy posting
    )

    app.test_client_class = FlaskLoginClient

    # holds context of the app for testing
    with app.app_context():
        # get the database object and create the tables inside the memory test-database
        from app import db
        db.init_app(app)  # relink it to the app to get the updated uri
        db.create_all()
        cust = Role(name='customer')
        merch = Role(name='merchant')
        db.session.add(cust)
        db.session.add(merch)
        db.session.commit()
    yield app

    # Can add cleanup here


@pytest.fixture()
def db(app):
    from app import db
    yield db


@pytest.fixture()
def client(app):
    return app.test_client()
