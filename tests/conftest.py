import pytest
from flask_login import FlaskLoginClient
from sqlalchemy import insert

from app import webapp
from app.models import User, UserRole


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
    yield app

    # Can add cleanup here


@pytest.fixture(scope="function")
def db(app):
    from app import db
    from app.models import Role, Category
    cust = Role(name='customer')
    merch = Role(name='merchant')
    admin = Role(name='admin')
    db.session.add(cust)
    db.session.add(merch)
    db.session.add(admin)

    categories = ["Clothing", "Video Games", "Electronics"]

    for category in categories:
        new_cat = Category(name=category)
        db.session.add(new_cat)

    # Create and register the admin
    user = User(username='admin', email='admin@test.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    # assign the merchant role to the user
    stmt = insert(UserRole).values(user_id=user.id, role_id=admin.id)
    db.session.execute(stmt)
    db.session.commit()

    db.session.commit()
    return db


@pytest.fixture()
def client(app):
    return app.test_client()
