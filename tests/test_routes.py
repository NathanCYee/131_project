import datetime

from sqlalchemy.orm import sessionmaker

from app.forms import DeleteAccountForm
from app.models import User, UserRole, Product, Order, OrderRow, Review, Discount
from sqlalchemy.orm import sessionmaker

from app.models import CartItem, Category, Order, OrderRow, Product, User, UserRole
from app.utils import create_discount


def test_home(client):
    with client:  # use for safety in case there are errors with the client
        response = client.get('/')  # act like a client and retrieve the site
        # must check a bytes object b"" instead of a string ""
        assert response.status_code == 200  # response.data returns the contents of the site


def test_good_login(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    # add a test user to the database
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    with client:
        response = client.get('/login')
        assert b'Login' in response.data

        response = client.post('/login',
                               data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        response = client.get('/account_test')
        assert response.status_code == 200  # successfully reached the test

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_bad_login(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    wrong_password = "pass-1"
    wrong_username = "test1"

    # add a test user to the database
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)

    with client:
        # test bad password
        response = client.post('/login',
                               data={'username': username, 'password': wrong_password, 'submit': True})
        assert response.status_code == 200  # 200 response ok, did not redirect
        # test bad username
        response = client.post('/login',
                               data={'username': wrong_username, 'password': password, 'submit': True})
        assert response.status_code == 200  # 200 response ok, did not redirect

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_logout(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    # add a test user to the database
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    with client:
        response = client.post('/login',
                               data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        response = client.get('/account_test')
        assert response.status_code == 200  # successfully reached the test

        client.get('/logout')  # call the logout

        response = client.get('/account_test')
        assert response.status_code != 200  # No longer reachable

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_good_register(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    with client:
        response = client.post('/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        response = client.get('/account_test')
        assert response.status_code == 200  # successfully reached the test

        # check to see if the user is in the database
        users = User.query.filter_by(username=username)
        assert users.count() == 1  # should only have 1 matching user

        # check props of user to make sure they are inserted correctly
        user = users.first()
        assert user.username == username
        assert user.email == email
        assert user.check_password(password)

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_bad_register(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    improper_email = "testmail"
    new_username = "Test2"

    # add a test user to the database
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    with client:
        # test for improperly formatted email (not verified)
        response = client.post('/register',
                               data={'username': new_username, 'email': improper_email, 'password': password,
                                     'submit': True})
        assert response.status_code == 200  # 200, did not redirect

        # test for an already existing account
        response = client.post('/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 200  # 200, did not redirect
        assert b"Username is already taken" in response.data

        # test for an already existing email
        response = client.post('/register',
                               data={'username': new_username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 200  # 200, did not redirect
        assert b"Email has already been used" in response.data

        # check to see if the user is in the database
        users = User.query.filter_by(username=username)
        assert users.count() == 1  # should only have 1 matching user

        # check props of user to make sure they are inserted correctly
        user = users.first()
        assert user.username == username
        assert user.email == email
        assert user.check_password(password)

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_account_info(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    new_password = "Pass-2"

    success_message = b"Password successfully changed"

    # add a test user to the database
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    with client:
        response = client.post('/login',
                               data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302  # successful login, redirected to homepage

        response = client.get('/account_info')
        assert response.status_code == 200  # Successful update
        assert bytes(user.username, 'utf-8') in response.data
        assert bytes(user.email, 'utf-8') in response.data

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_good_password_update(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    new_password = "Pass-2"

    success_message = b"Password successfully changed"

    # add a test user to the database
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    with client:
        response = client.post('/login',
                               data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302  # successful login, redirected to homepage

        response = client.post('/account_info', data={'original_password': password, 'new_password': new_password,
                                                      'new_password_repeat': new_password, 'submit': True})
        assert response.status_code == 200  # Successful update
        assert success_message in response.data  # check to see if the alert is in the returned page

        check_user = User.query.filter_by(id=user.id).first()
        assert check_user.check_password(new_password)  # check to ensure that password is updated

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_bad_password_update(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    bad_password = "password"
    new_password = "Pass-2"
    missed_password = "Pass2"

    failure_message_1 = b"Passwords do not match"
    failure_message_2 = b"Incorrect password. Please enter your original password."

    # add a test user to the database
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    with client:
        response = client.post('/login',
                               data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302  # successful login, redirected to homepage

        # Check to ensure that password mismatch is caught
        response = client.post('/account_info', data={'original_password': password, 'new_password': new_password,
                                                      'new_password_repeat': missed_password, 'submit': True})
        assert response.status_code == 200  # Sent back to account info with an error
        assert failure_message_1 in response.data  # check to see if the alert is in the returned page

        check_user = User.query.filter_by(id=user.id).first()
        assert check_user.check_password(password)  # check to ensure that password is not modified

        # Check to ensure that original password has to be present
        response = client.post('/account_info', data={'original_password': bad_password, 'new_password': new_password,
                                                      'new_password_repeat': new_password, 'submit': True})
        assert response.status_code == 200  # Sent back to account info with an error
        assert failure_message_2 in response.data  # check to see if the alert is in the returned page

        check_user = User.query.filter_by(id=user.id).first()
        assert check_user.check_password(password)  # check to ensure that password is not modified

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_delete_account(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    # add a test user to the database
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    with client:
        response = client.post('/login',
                               data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302  # successful login, redirected to homepage

        response = client.get('/account_test')
        assert response.status_code == 200  # successfully reached the test

        response = client.get('/delete_account')
        assert b"I want to delete my account." in response.data

        response = client.post('/delete_account', data={'confirm': True, 'submit': True})
        assert response.status_code == 302  # Redirected to login page

        response = client.get('/account_test')
        assert response.status_code != 200  # failed to reach the test, user no longer logged in

        user_count = User.query.filter_by(id=user.id).count()  # find the account with the unique id
        assert user_count == 0  # check to ensure that the account is successfully removed from the database

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_product_page(db, client):
    # test params
    search_query = "cool"
    search_query2 = "(c|C)ool"

    name = "Cool shirt"
    product_price = 999.99
    description = """Lorem ipsum dolor sit amet, consectetur adipiscing elit."""

    # create the product
    product = Product(merchant_id=0, name=name, price=product_price, description=description,
                      category_id=1)
    db.session.add(product)
    db.session.commit()
    with client:
        response = client.get(f'/product/{product.id}')
        assert response.status_code == 200
        assert bytes(product.name, 'utf-8') in response.data
        assert bytes(f"{product.price:.2f}", 'utf-8') in response.data
        assert bytes(product.description, 'utf-8') in response.data

        response = client.get('/product/10000')
        assert response.status_code == 404


def test_search(db, client):
    # test params
    search_query = "cool"
    search_query2 = "(c|C)ool"

    name = "Cool shirt"
    product_price = 999.99
    description = """Lorem ipsum dolor sit amet, consectetur adipiscing elit."""

    # create the product
    product = Product(merchant_id=0, name=name, price=product_price, description=description,
                      category_id=1)
    db.session.add(product)
    db.session.commit()

    query_result = Product.query.filter_by(name=name)

    # test to make sure it has been inserted
    assert query_result.count() == 1
    assert query_result.first() == product

    name2 = "cooler shirt"
    product_price2 = 10000
    description2 = """Maecenas dapibus ac mauris ac commodo."""

    # create the product
    product2 = Product(merchant_id=0, name=name2, price=product_price2, description=description2,
                       category_id=1)
    db.session.add(product2)
    db.session.commit()

    query_result = Product.query.all()

    # test to make sure it has been inserted
    assert len(query_result) == 2

    with client:
        response = client.get('/search/', query_string={'q': search_query})
        assert response.status_code == 200

        # should only have `cool` and not `Cool`
        assert bytes(name2, 'utf-8') in response.data
        assert bytes(name, 'utf-8') not in response.data

        response = client.get('/search/', query_string={'q': search_query2})
        assert response.status_code == 200

        # should have both `cool` and `Cool`
        assert bytes(name2, 'utf-8') in response.data
        assert bytes(name, 'utf-8') in response.data

        response = client.get('/search', query_string={'q': ''})
        assert response.status_code == 200


def test_client_order(db, client):
    # test customer params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    cust_address = "123 Sesame Street."

    Session = sessionmaker(db.engine)
    with Session() as session:
        # create the customer
        user = User(username=username, email=email)
        user.set_password(password)
        session.add(user)

        name = "Cool shirt"
        product_price = 999.99
        description = """Lorem ipsum dolor sit amet, consectetur adipiscing elit."""

        # create the product
        product = Product(merchant_id=0, name=name, price=product_price, description=description,
                          category_id=1)
        session.add(product)
        session.commit()

        query_result = Product.query.filter_by(name=name)
        with client:
            response = client.post('/login',
                                   data={'username': username, 'password': password, 'submit': True})
            assert response.status_code == 302  # 302 successful redirect to home page

            order = Order(user_id=user.id, ship_address=cust_address)
            session.add(order)
            session.commit()
            test_row = OrderRow(id=order.id, product_id=product.id, quantity=1, product_price=product.price)
            session.add(test_row)
            session.commit()

            # unfilled order
            assert not test_row.filled

            # check if the user can see their unfilled orders
            response = client.get('/orders')
            assert response.status_code == 200
            # check to see if info from the order is in the page
            assert bytes(product.name, 'utf-8') in response.data
            assert bytes(str(test_row.quantity), 'utf-8') in response.data
            assert bytes(f'{test_row.product_price:.2f}', 'utf-8') in response.data

            # merchant fills their order
            test_row.filled = True
            session.commit()

            # check to see if info from the order removed from the page
            response = client.get('/orders')
            assert bytes(product.name, 'utf-8') not in response.data

            # make sure order becomes filled
            find_row = OrderRow.query.filter_by(id=test_row.id).first()
            assert find_row.filled

            # check to see if the order is seen as filled by the customer
            response = client.get('/orders/filled')
            assert bytes(product.name, 'utf-8') in response.data

        # clean up any changes
        User.query.delete()
        Product.query.delete()
        Order.query.delete()
        OrderRow.query.delete()
        db.session.query(UserRole).delete()
        db.session.commit()
        db.session.flush()


def test_review(db, client):
    # test params
    username = "Test1"
    password = "Pass-1"
    username2 = "Test2"
    password2 = "Pass-2"
    username3 = "Test3"
    password3 = "Pass-3"
    username4 = "Test4"
    password4 = "Pass-4"

    # add test users to the database
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    user2 = User(username=username2)
    user2.set_password(password2)
    db.session.add(user2)
    user3 = User(username=username3)
    user3.set_password(password3)
    db.session.add(user3)
    user4 = User(username=username4)
    user4.set_password(password4)
    db.session.add(user4)
    db.session.commit()

    # add a test product, order, and orderrow
    name = "Cool shirt"
    product_price = 999.99
    description = """Lorem ipsum dolor sit amet, consectetur adipiscing elit."""

    # create the product
    product = Product(merchant_id=0, name=name, price=product_price, description=description,
                      category_id=1)
    db.session.add(product)
    order = Order(user_id=user.id)
    db.session.add(order)
    db.session.commit()
    order_row = OrderRow(id=order.id, product_id=product.id)
    db.session.add(order_row)
    order2 = Order(user_id=user2.id)
    db.session.add(order2)
    db.session.commit()
    order_row2 = OrderRow(id=order2.id, product_id=product.id)
    db.session.add(order_row2)
    order3 = Order(user_id=user3.id)
    db.session.add(order3)
    db.session.commit()
    order_row3 = OrderRow(id=order3.id, product_id=product.id)
    db.session.add(order_row3)
    db.session.commit()

    with client:
        response = client.post('/login',
                               data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        client.post(f'/product/{product.id}/review', data={'rating': '5', 'body': 'Awesome!', 'submit': True})
        response = client.get(f'/product/{product.id}/')
        assert b'5.0' in response.data
        assert b'Test1' in response.data
        assert b'5' in response.data
        assert b'Awesome!' in response.data

        client.get('/logout')  # call the logout

        response = client.post('/login',
                               data={'username': username2, 'password': password2, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        client.post(f'/product/{product.id}/review', data={'rating': '1', 'body': 'Terrible!', 'submit': True})
        response = client.get(f'/product/{product.id}/')
        assert b'3.0' in response.data
        assert b'Test2' in response.data
        assert b'1' in response.data
        assert b'Terrible!' in response.data

        client.get('/logout')  # call the logout

        response = client.post('/login',
                               data={'username': username3, 'password': password3, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        client.post(f'/product/{product.id}/review', data={'rating': '1', 'body': 'Awful!', 'submit': True})
        response = client.get(f'/product/{product.id}')
        assert b'2.3' in response.data
        assert b'Test3' in response.data
        assert b'1' in response.data
        assert b'Awful!' in response.data

        client.post(f'/product/{product.id}/review', data={'rating': '2', 'body': 'Not THAT awful.', 'submit': True})
        response = client.get(f'/product/{product.id}')
        assert b'You&#39;ve already reviewed this product' in response.data

        client.get('/logout')  # call the logout

        response = client.post('/login',
                               data={'username': username4, 'password': password4, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        client.post(f'/product/{product.id}/review', data={'rating': '4', 'body': 'I like this.', 'submit': True})
        response = client.get(f'/product/{product.id}')
        assert b'You need to have bought an item to review it.' in response.data

    # clean up any changes
    User.query.delete()
    Product.query.delete()
    Order.query.delete()
    OrderRow.query.delete()
    Review.query.delete()
    db.session.commit()
    db.session.flush()


def test_add_cart(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    # add a test user to the database
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)

    # make product
    product = Product(id=321, category_id=321, merchant_id=123,
                      name="iPhone", price=999.99, description="Lorem ipsum")
    db.session.add(product)

    # commit to database
    db.session.commit()

    with client:
        request = client.post('/login',
                              data={'username': username, 'password': password, 'submit': True})
        assert request.status_code == 302  # successful login, redirected to homepage

        request = client.post('/cart',
                              data={'product_id': product.id, 'quantity': 1, 'submit': True})
        assert request.status_code == 302  # successful redirect to cart page

        # get the user after the item was added to cart
        user = User.query.filter_by(username=username).first()

        cart_items = user.cart_items
        assert cart_items.count() == 1
        assert cart_items.first().product_id == product.id

        # clean up changes
        User.query.delete()
        Product.query.delete()
        CartItem.query.delete()
        db.session.query(UserRole).delete()
        db.session.commit()
        db.session.flush()


def test_cart_remove(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    # add a test user to the database
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)

    # make product
    product = Product(id=321, category_id=321, merchant_id=123,
                      name="iPhone", price=999.99, description="Lorem ipsum")
    db.session.add(product)

    # commit to database
    db.session.commit()

    with client:
        request = client.post('/login',
                              data={'username': username, 'password': password, 'submit': True})
        assert request.status_code == 302  # successful login, redirected to homepage

        request = client.post('/cart',
                              data={'product_id': product.id, 'quantity': 1, 'submit': True})
        assert request.status_code == 302  # successful redirect to cart page

        # get the user after the item was added to cart
        user = User.query.filter_by(username=username).first()

        cart_items = user.cart_items
        cart_row = cart_items.first()
        assert cart_items.count() == 1
        assert cart_row.product_id == product.id

        request = client.get(f'/cart/remove/{cart_row.id}')
        assert request.status_code == 302
        user = User.query.filter_by(username=username).first()

        cart_items = user.cart_items
        assert cart_items.count() == 0

        new_row = CartItem(id=5, product_id=product.id, user_id=5, quantity=10)
        db.session.add(new_row)
        db.session.commit()
        request = client.get(f'/cart/remove/{new_row.id}')
        assert request.status_code == 403

        # clean up changes
        User.query.delete()
        Product.query.delete()
        CartItem.query.delete()
        db.session.query(UserRole).delete()
        db.session.commit()
        db.session.flush()


def test_checkout(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    test_addr = "test_blvd"

    with client:
        # add a test user to the database
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)

        # make product
        product = Product(id=321, category_id=321, merchant_id=123,
                          name="iPhone", price=999.99, description="Lorem ipsum")
        db.session.add(product)

        # commit to database
        db.session.commit()

        request = client.post('/login',
                              data={'username': username, 'password': password, 'submit': True})
        assert request.status_code == 302  # successful login, redirected to homepage

        request = client.post('/cart',
                              data={'product_id': product.id, 'quantity': 1, 'submit': True})
        assert request.status_code == 302  # successful redirect to cart page

        request = client.post('/checkout',
                              data={'billing': '123456789', 'address': test_addr, 'submit': True})

        user = User.query.filter_by(username=user.username).first()

        # user should have no cartitems left
        assert user.cart_items.count() == 0

        # order created matching user id
        orders = Order.query.filter_by(user_id=user.id)
        assert orders.count() == 1

        order = orders.first()
        assert order.ship_address == test_addr

        # order row created with matching product id
        order_rows = order.order_row
        assert OrderRow.query.all()
        assert order_rows.all()
        assert order_rows.first().product_id == product.id

        # cart should be empty, test to make sure client cannot access checkout page with empty cart
        request = client.get('/checkout')
        assert request.status_code == 302

    # clean up changes
    User.query.delete()
    Product.query.delete()
    CartItem.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_category(db, client):
    category_name = "Electronics"
    category = Category.query.filter_by(name=category_name).first()

    # test params
    name = "iPhone 1000"
    product_price = 999.99
    description = "The brand new iPhone. Lorem ipsum sit amet."

    # create the product
    product = Product(merchant_id=0, name=name, price=product_price, description=description,
                      category_id=category.id)
    db.session.add(product)
    db.session.commit()

    query_result = Product.query.filter_by(name=name)

    with client:
        response = client.get(f'/category/{category.id}')
        assert bytes(category.name, 'utf-8') in response.data
        assert bytes(product.name, 'utf-8') in response.data

    # reset the state of the db
    Product.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_merchant_profile(db, client):
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    Session = sessionmaker(db.engine)
    with Session() as session:
        category_name = "Electronics"
        category = Category.query.filter_by(name=category_name).first()

        # test params
        name = "iPhone 1000"
        product_price = 999.99
        description = "The brand new iPhone. Lorem ipsum sit amet."

        with client:
            response = client.post('/merchant/register',
                                   data={'username': username, 'email': email, 'password': password, 'submit': True})
            assert response.status_code == 302  # 302 successful redirect to home page
            # check to see if the user is in the database

            user = User.query.filter_by(username=username).first()

            # create the product
            product = Product(merchant_id=user.id, name=name, price=product_price, description=description,
                              category_id=category.id)
            session.add(product)
            session.commit()

            response = client.get(f'/merchant/{user.id}')
            assert bytes(user.username, 'utf-8') in response.data
            assert bytes(product.name, 'utf-8') in response.data

    # reset the state of the db
    User.query.delete()
    Product.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_apply_discount(db, client):
    category_name = "Electronics"
    category = Category.query.filter_by(name=category_name).first()

    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    test_addr = "test_blvd"
    name = "iPhone 1000"
    product_price = 999.99
    description = "The brand new iPhone. Lorem ipsum sit amet."
    promo_name = "CODE10"
    discount_amount = 10
    expiration_date = datetime.date.today() + datetime.timedelta(days=10)

    Session = sessionmaker(db.engine)
    with Session() as session:
        # add a test user to the database
        user = User(username=username, email=email)
        user.set_password(password)
        session.add(user)
        session.commit()

        # create the product
        product = Product(merchant_id=0, name=name, price=product_price, description=description,
                          category_id=category.id)
        session.add(product)
        session.commit()

        applicable_products = [product.id]

        # create the discount
        discount = create_discount(code=promo_name, type=0, applicable_ids=applicable_products, percentage=False,
                                   amount=
                                   discount_amount, end_date=expiration_date)
        session.add(discount)
        session.commit()

        with client:
            request = client.post('/login',
                                  data={'username': username, 'password': password, 'submit': True})
            assert request.status_code == 302  # successful login, redirected to homepage

            # add to cart
            request = client.post('/cart',
                                  data={'product_id': product.id, 'quantity': 1, 'submit': True}, follow_redirects=True)

            # go to checkout with normal price
            request = client.get('/checkout')
            assert bytes(f"${product.price:.2f}", "utf-8") in request.data

            assert discount.apply_discount(user.cart_items[0].id) != 0

            # apply discount
            request = client.get('/checkout', query_string={'code': discount.code}, follow_redirects=True)
            assert bytes(discount.code, "utf-8") in request.data
            assert b"Applied discount" in request.data
            assert bytes(f"${product.price - discount_amount:.2f}", "utf-8") in request.data

            # apply bad discount
            request = client.get('/checkout', query_string={'code': "FAKE_DEAL"}, follow_redirects=True)
            assert b"is not valid" in request.data

            # checkout with a discount
            request = client.post(f'/checkout',
                                  data={'discount_code': discount.code,
                                        'billing': '123456789', 'address': test_addr, 'submit': True})
            assert request.status_code == 302  # redirect to orders page

            orders = user.orders
            assert orders.count() == 1
            order_row = orders.first().order_row
            assert order_row.count() == 1
            first_row = order_row.first()
            assert first_row.product_price == product.price - discount_amount

    # reset the state of the db
    User.query.delete()
    Product.query.delete()
    Discount.query.delete()
    Order.query.delete()
    OrderRow.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_apply_category_discount(db, client):
    category_name = "Electronics"
    category = Category.query.filter_by(name=category_name).first()

    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    test_addr = "test_blvd"
    name = "iPhone 1000"
    product_price = 999.99
    description = "The brand new iPhone. Lorem ipsum sit amet."
    promo_name = "CODE10"
    discount_amount = 10
    expiration_date = datetime.date.today() + datetime.timedelta(days=10)

    Session = sessionmaker(db.engine)
    with Session() as session:
        # add a test user to the database
        user = User(username=username, email=email)
        user.set_password(password)
        session.add(user)
        session.commit()

        # create the product
        product = Product(merchant_id=0, name=name, price=product_price, description=description,
                          category_id=category.id)
        session.add(product)
        session.commit()

        applicable_products = [category.id]

        # create the discount
        discount = create_discount(code=promo_name, type=1, applicable_ids=applicable_products, percentage=False,
                                   amount=
                                   discount_amount, end_date=expiration_date)
        session.add(discount)
        session.commit()

        with client:
            request = client.post('/login',
                                  data={'username': username, 'password': password, 'submit': True})
            assert request.status_code == 302  # successful login, redirected to homepage

            # add to cart
            request = client.post('/cart',
                                  data={'product_id': product.id, 'quantity': 1, 'submit': True}, follow_redirects=True)

            # go to checkout with normal price
            request = client.get('/checkout')
            assert bytes(f"${product.price:.2f}", "utf-8") in request.data

            assert discount.apply_discount(user.cart_items[0].id) != 0

            # apply discount
            request = client.get('/checkout', query_string={'code': discount.code}, follow_redirects=True)
            assert bytes(discount.code, "utf-8") in request.data
            assert b"Applied discount" in request.data
            assert bytes(f"${product.price - discount_amount:.2f}", "utf-8") in request.data

            # apply bad discount
            request = client.get('/checkout', query_string={'code': "FAKE_DEAL"}, follow_redirects=True)
            assert b"is not valid" in request.data

            # checkout with a discount
            request = client.post(f'/checkout',
                                  data={'discount_code': discount.code,
                                        'billing': '123456789', 'address': test_addr, 'submit': True})
            assert request.status_code == 302  # redirect to orders page

            orders = user.orders
            assert orders.count() == 1
            order_row = orders.first().order_row
            assert order_row.count() == 1
            first_row = order_row.first()
            assert first_row.product_price == product.price - discount_amount

    # reset the state of the db
    User.query.delete()
    Product.query.delete()
    Discount.query.delete()
    Order.query.delete()
    OrderRow.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_apply_sitewide_discount(db, client):
    category_name = "Electronics"
    category = Category.query.filter_by(name=category_name).first()

    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    test_addr = "test_blvd"
    name = "iPhone 1000"
    product_price = 999.99
    description = "The brand new iPhone. Lorem ipsum sit amet."
    promo_name = "CODE10"
    discount_amount = 10
    expiration_date = datetime.date.today() + datetime.timedelta(days=10)

    Session = sessionmaker(db.engine)
    with Session() as session:
        # add a test user to the database
        user = User(username=username, email=email)
        user.set_password(password)
        session.add(user)
        session.commit()

        # create the product
        product = Product(merchant_id=0, name=name, price=product_price, description=description,
                          category_id=category.id)
        session.add(product)
        session.commit()

        # create the discount
        discount = create_discount(code=promo_name, type=2, applicable_ids=[], percentage=False,
                                   amount=
                                   discount_amount, end_date=expiration_date)
        session.add(discount)
        session.commit()

        with client:
            request = client.post('/login',
                                  data={'username': username, 'password': password, 'submit': True})
            assert request.status_code == 302  # successful login, redirected to homepage

            # add to cart
            request = client.post('/cart',
                                  data={'product_id': product.id, 'quantity': 1, 'submit': True}, follow_redirects=True)

            # go to checkout with normal price
            request = client.get('/checkout')
            assert bytes(f"${product.price:.2f}", "utf-8") in request.data

            assert discount.apply_discount(user.cart_items[0].id) != 0

            # apply discount
            request = client.get('/checkout', query_string={'code': discount.code}, follow_redirects=True)
            assert bytes(discount.code, "utf-8") in request.data
            assert b"Applied discount" in request.data
            assert bytes(f"${product.price - discount_amount:.2f}", "utf-8") in request.data

            # apply bad discount
            request = client.get('/checkout', query_string={'code': "FAKE_DEAL"}, follow_redirects=True)
            assert b"is not valid" in request.data

            # checkout with a discount
            request = client.post(f'/checkout',
                                  data={'discount_code': discount.code,
                                        'billing': '123456789', 'address': test_addr, 'submit': True})
            assert request.status_code == 302  # redirect to orders page

            orders = user.orders
            assert orders.count() == 1
            order_row = orders.first().order_row
            assert order_row.count() == 1
            first_row = order_row.first()
            assert first_row.product_price == product.price - discount_amount

    # reset the state of the db
    User.query.delete()
    Product.query.delete()
    Discount.query.delete()
    Order.query.delete()
    OrderRow.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_apply_sitewide_percentage_discount(db, client):
    category_name = "Electronics"
    category = Category.query.filter_by(name=category_name).first()

    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    test_addr = "test_blvd"
    name = "iPhone 1000"
    product_price = 1000
    description = "The brand new iPhone. Lorem ipsum sit amet."
    promo_name = "CODE10"
    discount_amount = 10
    expiration_date = datetime.date.today() + datetime.timedelta(days=10)

    Session = sessionmaker(db.engine)
    with Session() as session:
        # add a test user to the database
        user = User(username=username, email=email)
        user.set_password(password)
        session.add(user)
        session.commit()

        # create the product
        product = Product(merchant_id=0, name=name, price=product_price, description=description,
                          category_id=category.id)
        session.add(product)
        session.commit()

        # create the discount
        discount = create_discount(code=promo_name, type=2, applicable_ids=[], percentage=True,
                                   amount=
                                   discount_amount/100, end_date=expiration_date)
        session.add(discount)
        session.commit()

        with client:
            request = client.post('/login',
                                  data={'username': username, 'password': password, 'submit': True})
            assert request.status_code == 302  # successful login, redirected to homepage

            # add to cart
            request = client.post('/cart',
                                  data={'product_id': product.id, 'quantity': 1, 'submit': True}, follow_redirects=True)

            # go to checkout with normal price
            request = client.get('/checkout')
            assert bytes(f"${product.price:.2f}", "utf-8") in request.data

            assert discount.apply_discount(user.cart_items[0].id) != 0

            # apply discount
            request = client.get('/checkout', query_string={'code': discount.code}, follow_redirects=True)
            assert bytes(discount.code, "utf-8") in request.data
            assert b"Applied discount" in request.data
            assert bytes(f"${product.price*((100-discount_amount)/100):.2f}", "utf-8") in request.data

            # apply bad discount
            request = client.get('/checkout', query_string={'code': "FAKE_DEAL"}, follow_redirects=True)
            assert b"is not valid" in request.data

            # checkout with a discount
            request = client.post(f'/checkout',
                                  data={'discount_code': discount.code,
                                        'billing': '123456789', 'address': test_addr, 'submit': True})
            assert request.status_code == 302  # redirect to orders page

            orders = user.orders
            assert orders.count() == 1
            order_row = orders.first().order_row
            assert order_row.count() == 1
            first_row = order_row.first()
            assert first_row.product_price == product.price*((100-discount_amount)/100)

    # reset the state of the db
    User.query.delete()
    Product.query.delete()
    Discount.query.delete()
    Order.query.delete()
    OrderRow.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_admin_discount(db, client):
    promo_name = "CODE10"
    promo_name2 = "CODE5"
    discount = 10

    expiration_date = datetime.date.today() + datetime.timedelta(days=10)

    Session = sessionmaker(db.engine)
    with Session() as session:
        category = Category.query.filter_by(name="Electronics").first()
        with client:
            request = client.post('/login',
                                  data={'username': 'admin', 'password': 'password', 'submit': True})
            assert request.status_code == 302  # successful login, redirected to homepage

            # post a response to the new promo site
            response = client.post('/admin/promo/',
                                   data={'code': promo_name, 'amount': discount, 'products': [category.id],
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)

            discounts = Discount.query.filter_by(code=promo_name)
            assert discounts.count() == 1
            discount = discounts.all()[0]
            assert discount.code == promo_name
            assert discount.is_valid()
            assert discount.details["type"] == 1

            # post a response to the new promo site
            response = client.post('/admin/promo/',
                                   data={'code': promo_name2, 'amount': discount, 'products': [-1],
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)

            discounts = Discount.query.filter_by(code=promo_name2)
            assert discounts.count() == 1
            discount = discounts.all()[0]
            assert discount.code == promo_name2
            assert discount.is_valid()
            assert discount.details["type"] == 2

    Discount.query.delete()
    db.session.commit()
    db.session.flush()


def test_admin_percentage_discount(db, client):
    promo_name = "CODE10"
    promo_name2 = "CODE5"
    discount_amount = 10

    expiration_date = datetime.date.today() + datetime.timedelta(days=10)

    Session = sessionmaker(db.engine)
    with Session() as session:
        category = Category.query.filter_by(name="Electronics").first()
        with client:
            request = client.post('/login',
                                  data={'username': 'admin', 'password': 'password', 'submit': True})
            # post a response to the new promo site
            response = client.post('/admin/promo/percentage/',
                                   data={'code': promo_name, 'amount': discount_amount, 'products': [category.id],
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)

            discounts = Discount.query.filter_by(code=promo_name)
            assert discounts.count() == 1
            discount = discounts.all()[0]
            assert discount.code == promo_name
            assert discount.is_valid()
            assert discount.details["type"] == 1
            assert discount.details["percentage"]

            # post a response to the new promo site
            response = client.post('/admin/promo/percentage/',
                                   data={'code': promo_name2, 'amount': discount_amount, 'products': [-1],
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)

            discounts = Discount.query.filter_by(code=promo_name2)
            assert discounts.count() == 1
            discount = discounts.all()[0]
            assert discount.code == promo_name2
            assert discount.is_valid()
            assert discount.details["type"] == 2
            assert discount.details["percentage"]

    Discount.query.delete()
    db.session.commit()
    db.session.flush()


def test_bad_admin_discount(db, client):
    promo_name = "CODE10"
    promo_name2 = "CODE5"
    discount = 10
    big_discount = 10000

    expiration_date = datetime.date.today() + datetime.timedelta(days=10)

    Session = sessionmaker(db.engine)
    with Session() as session:
        # test product params
        name = "iPhone"
        product_price = 999.99
        description = "The brand new iPhone. Lorem ipsum sit amet."
        with client:
            request = client.post('/login',
                                  data={'username': 'admin', 'password': 'password', 'submit': True})
            # post a good promo
            response = client.post('/admin/promo',
                                   data={'code': promo_name, 'amount': discount, 'products': [1],
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)

            discounts = Discount.query.filter_by(code=promo_name)
            assert discounts.count() == 1
            discount = discounts.all()[0]
            assert discount.code == promo_name
            assert discount.is_valid()

            # post a promo with the same code
            response = client.post('/admin/promo',
                                   data={'code': promo_name, 'amount': discount, 'products': [1],
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)

            discounts = Discount.query.filter_by(code=promo_name)
            assert discounts.count() == 1

            # post a promo with a large percentage value
            response = client.post('/admin/promo/percentage',
                                   data={'code': promo_name2, 'amount': big_discount, 'products': [1],
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)

            discounts = Discount.query.filter_by(code=promo_name2)
            assert discounts.count() == 0

    User.query.delete()
    Product.query.delete()
    Discount.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_product_page(db, client):
    # test account params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    # test product params
    name = "iPhone"
    price = 999.99
    description = "The brand new iPhone. Lorem ipsum sit amet."
    category = Category.query.filter_by(name="Electronics").first()
    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        user = User.query.filter_by(username=username).first()

        response = client.post('/merchant/new_product',
                               data={'merchant_id': user.id, 'name': name, 'price': price, 'description': description,
                                     'category': category.name, 'pictures': [], 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to product page
        response = client.get('/logout')

        products = Product.query.filter_by(name=name)
        assert products.count() == 1
        product = products.first()
        response = client.get(f'/product/{product.id}', follow_redirects=True)
        assert bytes(product.name, 'utf-8') in response.data
        assert bytes(product.description, 'utf-8') in response.data

        # make sure the site returns 404 if not found
        response = client.get(f'/product/40000', follow_redirects=True)
        assert response.status_code == 404
    # clean up any changes
    User.query.delete()
    Product.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_discount_page(db, client):
    category_name = "Electronics"
    category = Category.query.filter_by(name=category_name).first()

    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    test_addr = "test_blvd"
    name = "iPhone 1000"
    product_price = 999.99
    description = "The brand new iPhone. Lorem ipsum sit amet."
    promo_name = "CODE10"
    promo_name2 = "ELECTRONICS10"
    promo_name3 = "10OFF"
    discount_amount = 10
    expiration_date = datetime.date.today() + datetime.timedelta(days=10)

    Session = sessionmaker(db.engine)
    with Session() as session:
        # add a test user to the database
        user = User(username=username, email=email)
        user.set_password(password)
        session.add(user)
        session.commit()

        # create the product
        product = Product(merchant_id=0, name=name, price=product_price, description=description,
                          category_id=category.id)
        session.add(product)
        session.commit()

        # create the product discount
        discount = create_discount(code=promo_name, type=0, applicable_ids=[product.id], percentage=False,
                                   amount=
                                   discount_amount, end_date=expiration_date)
        session.add(discount)
        session.commit()

        # create the category discount
        discount = create_discount(code=promo_name2, type=1, applicable_ids=[category.id], percentage=False,
                                   amount=
                                   discount_amount, end_date=expiration_date)
        session.add(discount)
        session.commit()

        # create the sitewide discount
        discount = create_discount(code=promo_name3, type=2, applicable_ids=[], percentage=True,
                                   amount=
                                   discount_amount, end_date=expiration_date)
        session.add(discount)
        session.commit()

        with client:
            results = client.get('/discounts')
            assert bytes(promo_name, 'utf-8') in results.data
            assert bytes(promo_name2, 'utf-8') in results.data
            assert bytes(promo_name3, 'utf-8') in results.data
            assert b"$10.00" in results.data
            assert b"%" in results.data

    Product.query.delete()
    Discount.query.delete()
    Order.query.delete()
    OrderRow.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_admin_redirect(client):
    with client:
        response = client.get('/admin/promo')
        assert response.status_code == 302
