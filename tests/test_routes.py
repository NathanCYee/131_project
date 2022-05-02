from app.models import CartItem, Product, User, UserRole


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

def test_add_cart(db, client):
    #test account params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    #test cart params
    quantity = 1
    product_id = Product.query.filter_by(id=321)

    with client:
        response = client.post('/login',
                                data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302 # successful login, redirected to homepage

        user = User.query.filter_by(username=username).first()
        
        response = client.post('/cart', 
                                data={'product_id': product_id, 'quantity': quantity, 'submit': True})
        assert response.status_code == 302 # successful redirect to cart page

        cart_item = CartItem.query.filter_by(product_id=product_id)
        assert cart_item.count == 1

        #clean up changes
        User.query.delete()
        CartItem.query.delete()
        db.session.query(UserRole).delete()
        db.session.commit()
        db.session.flush()