import pytest
from tests.conftest import *


def test_home(client):
    response = client.get('/')  # act like a client and retrieve the site
    # must check a bytes object b"" instead of a string ""
    assert b"<div>Inside the div</div>" in response.data  # response.data returns the contents of the site
