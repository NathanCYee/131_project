from app.models import User


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

    with client:
        response = client.post('/login',
                               data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page
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
    db.session.flush()
