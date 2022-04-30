# Unit testing

## Table of contents

- [Running tests](https://github.com/NathanCYee/131_project/tests#running-tests)
- [Creating tests](https://github.com/NathanCYee/131_project/tests#creating-tests)
- [Continuous integration](https://github.com/NathanCYee/131_project/tests#continuous-integration)

## Running tests

Please make sure pytest and pytest-cov are installed. From the parent directory of tests, run the tests using `pytest`.
If coverage is needed, run with coverage using `pytest --cov=app`.

## Creating tests

### Naming tests

In order for the `pytest` command to detect your test, name your test function starting with `test_`.

```
def test_...():
```

### Fixtures

Several fixtures are available in conftest.py that are available for use.

- `app` - This returns a Flask app instance for testing. The app is configured with a changed testing state, a changed
  database url (set to an in-memory SQLite database `"sqlite:///:memory:"`), and disabled CSRF so that form submits
  don't need to include the hidden key. This fixture is not of much use in tests.
- `db` - This returns a SQLAlchemy db object instance that can be accessed like a normal database instance (i.e.
  using `db.session`). The database is configured with `customer` and `merchant` roles for testing.
- `client` - This returns a client instance that can be used to test routes in the app.
    - `client.post("/path", data={})` - This will send a POST request to the path with the data. The data is a
      dictionary object that will represent the data sent by the form.
    - `client.get("/path", data={})` - This will send a GET request to the path with the data. The data is a dictionary
      object that will represent the data sent by the form.
    - Set the data received from the request to a variable in order to access the data that Flask returns to the
      request.
        - `response = client.post(...` - Will set the data received from the request to the variable `response`.
        - `response.data` - Will return the contents of the page received from the request (usually the contents of the
          html).
        - `response.status_code` - Will return
          the [HTTP status code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) of the response.

In order to use a fixture in a test, pass the name(s) of the fixture into the test function

```
def test_login(client, db):
    ...
```

In a test, open up a fixture using a `with` statement in order to save the context of the requests. This will allow you
to login to a user and use the page while logged in and perform possible cleanup operations.

```
def test_login(client):
    with client:
        # send a POST request to login and save the data recieved back to a variable
        response = client.post('/login', data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302  # Check the status code
```

If a database is modified, delete any inserted rows after the test is run using `Modelobj.query.delete()` and
using `db.session.flush()`. Be sure to commit the deletes.

```
def test_login(db):
    with db:
        ...
    User.query.delete()
    db.session.commit()
    db.session.flush()
```

## Continuous Integration

CircleCI automatically runs pytest and sends coverage to CircleCI on pull requests and commits to master. 