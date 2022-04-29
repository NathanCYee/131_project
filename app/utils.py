from functools import wraps
from flask import flash, redirect
from flask_login import current_user

from app.models import User, Product, Order, OrderRow, Role, Category


def get_merchant():
    return Role.query.filter_by(name='merchant').first()


def merchant_required(func):
    """decorator to require the current_user to have the merchant role or else it redirects"""

    @wraps(func)
    def inner(*args, **kwargs):

        if not current_user.is_authenticated or current_user.roles.filter_by(id=get_merchant().id).count() == 0:
            flash("You must be a merchant to access this page!")
            return redirect('/merchant/login')
        else:
            return func(*args, **kwargs)

    return inner


def create_order(user: User, products) -> Order:
    id = user.id


def get_categories():
    return [c.name for c in Category.query.all()]
