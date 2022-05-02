import pytest
from sqlalchemy import create_engine, inspect
from app.forms import CartForm
from app.models import CartItem, User, Category, Product, UserRole


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
    name = "Office Supplies"
    category = Category(name=name)
    db.session.add(category)
    query_result = Category.query.filter_by(name=name)

    # test to make sure it has been inserted
    assert query_result.count() == 1
    assert query_result.first() == category

    # reset the state of the db
    Category.query.filter_by(id=category.id).delete()
    db.session.flush()


def test_product(db):
    """Create a user object and input into the database. Assert to see if object is created."""
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    # create the user
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)

    category_name = "Electronics"
    category = Category.query.filter_by(name=category_name).first()

    # test params
    name = "iPhone 1000"
    product_price = 999.99
    description = "The brand new iPhone. Lorem ipsum sit amet."

    # create the product
    product = Product(merchant_id=user.id, name=name, price=product_price, description=description,
                      category_id=category.id)
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
    User.query.delete()
    Product.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


    def test_cartitem(db):
        """Create a user object and input into the database. Assert to see if object is created."""
        # test params
        username = "Test1"
        email = "test@email.com"
        password = "Pass-1"

        # create the user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)

        product = Product.query.filter_by(id=321).first()

        # test params
        quantity = 1
        
        # create the item
        cart_item = CartItem(product_id=product.id, user_id=user.id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()

        query_result = CartItem.query.filter_by(product_id=product.id)

        # testing to see if item has been added
        assert query_result.count() == 1
        assert query_result.first() == cart_item

        # reset state of database
        User.query.delete()
        CartItem.query.delete()
        db.session.query(UserRole).delete()
        db.session.commit()
        db.session.flush()