import pytest
from sqlalchemy import create_engine, inspect
from app.models import User, Category, Product


def test_db(db):
    """Check to see if the database fixture is linked to in-memory database"""
    engine = db.engine
    assert engine.url == create_engine("sqlite:///:memory:").url


def test_tables(db):
    """check to see if tables are successfully created"""
    inspector = inspect(db.engine)
    table_keys = inspector.get_table_names()
    assert 'user' in table_keys
    assert 'product' in table_keys
    assert 'cart_item' in table_keys
    assert 'order' in table_keys
    assert 'category' in table_keys
    assert 'review' in table_keys


def test_user(db):
    """Create a user object and input into the database. Assert to see if object is created."""

    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    # create the user
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    query_result = User.query.filter_by(username=username)

    # test to make sure it has been inserted
    assert query_result.count() == 1
    assert query_result.first() == user

    # reset the state of the db
    db.session.flush()


def test_category(db):
    name = "Video Games"
    category = Category(name=name)
    db.session.add(category)
    query_result = Category.query.filter_by(name=name)

    # test to make sure it has been inserted
    assert query_result.count() == 1
    assert query_result.first() == category

    # reset the state of the db
    db.session.flush()


def test_product(db):
    """Create a user object and input into the database. Assert to see if object is created."""

    category_name = "Devices"
    category = Category(name=category_name)
    db.session.add(category)
    db.session.commit()

    # test params
    name = "iPhone 1000"
    product_price = 999.99
    description = "The brand new iPhone. Lorem ipsum sit amet."

    # create the user
    product = Product(name=name, product_price=product_price, description=description, category_id=category.id)
    db.session.add(product)
    db.session.commit()

    query_result = Product.query.filter_by(name=name)

    # test to make sure it has been inserted
    assert query_result.count() == 1
    assert query_result.first() == product

    # check to make sure the category sees the model
    assert category.products.count() == 1
    assert category.products.first() == product

    # reset the state of the db
    db.session.flush()
