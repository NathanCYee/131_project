from app.models import User


def test_merchant_login(client):
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page
