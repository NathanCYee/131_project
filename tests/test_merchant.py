from app.models import User, UserRole, Product, Category


def test_merchant_denial(client):
    with client:
        response = client.get('/merchant')
        assert response.status_code == 302  # successfully reached the test


def test_merchant_register(db, client):
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page
        # check to see if the user is in the database

        response = client.get('/merchant/account_test')
        assert response.status_code == 200  # successfully reached the test

        response = client.get('/merchant')
        assert response.status_code == 200  # successfully reached the test

        users = User.query.filter(User.roles.any(id=2)).filter_by(username=username)
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

    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page
        client.get('/logout')  # call the logout

        # test for improperly formatted email (not verified)
        response = client.post('/merchant/register',
                               data={'username': new_username, 'email': improper_email, 'password': password,
                                     'submit': True})
        assert response.status_code == 200  # 200, did not redirect

        # test for an already existing account
        response = client.post('/merchant/register',
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


def test_good_login(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page
        client.get('/logout')  # call the logout

        response = client.post('/merchant/login',
                               data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        response = client.get('/merchant/account_test')
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

    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page
        client.get('/logout')  # call the logout

        # test bad password
        response = client.post('/merchant/login',
                               data={'username': username, 'password': wrong_password, 'submit': True})
        assert response.status_code == 200  # 200 response ok, did not redirect
        # test bad username
        response = client.post('/merchant/login',
                               data={'username': wrong_username, 'password': password, 'submit': True})
        assert response.status_code == 200  # 200 response ok, did not redirect
    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_add_product(db, client):
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
                                     'category': category.name, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to product page

        products = Product.query.filter_by(name=name)
        assert products.count() == 1

    # clean up any changes
    User.query.delete()
    Product.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()    