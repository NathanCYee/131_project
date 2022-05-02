from app.models import User, UserRole, Product, Order, OrderRow, Review
from flask import session
from sqlalchemy.orm import sessionmaker

from app.models import CartItem, Category, Order, OrderRow, Product, User, UserRole
from app.routes import category


def test_home(client):
    with client:  # use for safety in case there are errors with the client
        response = client.get('/')  # act like a client and retrieve the site
        # must check a bytes object b"" instead of a string ""
        assert b"</br>" in response.data  # response.data returns the contents of the site


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
        users = User.query.filter_by()
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
        print(response.data)
        assert response.status_code == 200  # successfully reached the test

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
    product = Product()
    db.session.add(product)
    order = Order(user_id=user.id)
    db.session.add(order)
    order_row = OrderRow(id=order.id, product_id=product.id)
    db.session.add(order_row)
    order2 = Order(user_id=user2.id)
    db.session.add(order2)
    order_row2 = OrderRow(id=order2.id, product_id=product.id)
    db.session.add(order_row2)
    order3 = Order(user_id=user3.id)
    db.session.add(order3)
    order_row3 = OrderRow(id=order3.id, product_id=product.id)
    db.session.add(order_row3)
    db.session.commit()

    with client:
        response = client.post('/login',
                               data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        client.post(f'/product/{product.id}/review', data={'rating': 5, 'body': 'Awesome!', 'submit': True})
        response = client.get(f'/product/{product.id}')
        assert b'5.0' in response.data
        assert b'Test1' in response.data
        assert b'5' in response.data
        assert b'Awesome!' in response.data

        client.get('/logout')  # call the logout

        response = client.post('/login',
                               data={'username': username2, 'password': password2, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        client.post(f'/product/{product.id}/review', data={'rating': 1, 'body': 'Terrible!', 'submit': True})
        response = client.get(f'/product/{product.id}')
        assert b'3.0' in response.data
        assert b'Test2' in response.data
        assert b'1' in response.data
        assert b'Terrible!' in response.data

        client.get('/logout')  # call the logout

        response = client.post('/login',
                               data={'username': username3, 'password': password3, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        client.post(f'/product/{product.id}/review', data={'rating': 1, 'body': 'Awful!', 'submit': True})
        response = client.get(f'/product/{product.id}')
        assert b'2.3' in response.data
        assert b'Test3' in response.data
        assert b'1' in response.data
        assert b'Awful!' in response.data

        client.post(f'/product/{product.id}/review', data={'rating': 2, 'body': 'Not THAT awful.', 'submit': True})
        response = client.get(f'/product/{product.id}')
        assert b'You&#39;ve already reviewed this product' in response.data

        client.get('/logout')  # call the logout

        response = client.post('/login',
                               data={'username': username4, 'password': password4, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        client.post(f'/product/{product.id}/review', data={'rating': 4, 'body': 'I like this.', 'submit': True})
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

    # clean up changes
    User.query.delete()
    Product.query.delete()
    CartItem.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()
