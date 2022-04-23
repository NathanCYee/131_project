import pytest
from app.models import User
from app.forms import LoginForm


def test_home(client):
    with client:  # use for safety in case there are errors with the client
        response = client.get('/')  # act like a client and retrieve the site
        # must check a bytes object b"" instead of a string ""
        assert b"</br>" in response.data  # response.data returns the contents of the site


def test_login(app, db):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)

    user_form = LoginForm(username=username, password=password)
    assert user_form.validate()
    with app.test_request_context(user=user) as client:
        assert client.get('/')
