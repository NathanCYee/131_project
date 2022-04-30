from functools import wraps
from flask import flash, redirect
from flask_login import current_user

from app.models import Role, Category


def get_merchant():
    """Retrieve a Role object representing a merchant"""
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


def prevent_merchant(func):
    """decorator to prevent merchants from accessing sites"""

    @wraps(func)
    def inner(*args, **kwargs):

        if current_user.is_authenticated and current_user.roles.filter_by(id=get_merchant().id).count() >= 1:
            flash("You cannot be logged in as a merchant!")
            return redirect('/login')
        else:
            return func(*args, **kwargs)

    return inner


def get_categories():
    """Retrieve a list of category names from the database"""
    return [c.name for c in Category.query.all()]


def get_category_dict():
    """Retrieve a dictionary of categories in the form name:id"""
    return {c.name: c.id for c in Category.query.all()}
