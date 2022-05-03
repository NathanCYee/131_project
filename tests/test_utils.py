from app.models import Category
from app.utils import get_categories, get_category_dict


def test_get_categories(db):
    res = get_categories()
    categories = ["Clothing", "Video Games", "Electronics"]
    for category in categories:
        assert category in categories


def test_get_category_dict(db):
    res = get_category_dict()
    categories = ["Clothing", "Video Games", "Electronics"]
    for category in categories:
        cat = Category.query.filter_by(name=category).first()
        assert category in res.keys()
        assert res[category] == cat.id


def test_prevent_merchant(client):
    with client:
        response = client.get('/merchant/account_test')
        assert response.status_code == 302
        response = client.get('/merchant/account_test', follow_redirects=True)
        assert response.request.path == '/merchant/login'
