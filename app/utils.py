from functools import wraps
from flask import flash, redirect
from flask_login import current_user

from app.models import Role, Category


def get_merchant():
    """
    Retrieve a Role object representing a merchant
    :return: a Role object with the name `merchant`
    """
    return Role.query.filter_by(name='merchant').first()


def merchant_required(func):
    """
    decorator to require the current_user to have the merchant role or else it redirects
    :param func: The function to decorate
    :return: A function instance that checks the current user is a merchant before returning the action
    """

    @wraps(func)
    def inner(*args, **kwargs):
        """
        :decorator: A decorator for a flask route function
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return: The correct page if the user is logged in as a merchant, redirection to the login page if otherwise
        """
        if not current_user.is_authenticated or current_user.roles.filter_by(id=get_merchant().id).count() == 0:
            flash("You must be a merchant to access this page!")
            return redirect('/merchant/login')
        else:
            return func(*args, **kwargs)

    return inner


def prevent_merchant(func):
    """
    decorator to prevent merchants from accessing sites
    :param func: func: The function to decorate
    :return: A function instance that checks the current user is not a merchant before returning the action
    """

    @wraps(func)
    def inner(*args, **kwargs):
        """
        :decorator: A decorator for a flask route function
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return: The correct page if the user is not logged in as a merchant, redirection if otherwise
        """
        if current_user.is_authenticated and current_user.roles.filter_by(id=get_merchant().id).count() >= 1:
            flash("You cannot be logged in as a merchant!")
            return redirect('/login')
        else:
            return func(*args, **kwargs)

    return inner


def get_categories():
    """
    Retrieve a list of category names from the database
    :return: A python list containing the string names of all the categories
    """
    return [c.name for c in Category.query.all()]


def get_category_dict():
    """
    Retrieve a dictionary of categories in the form name:id
    :return: A python dictionary with key=category name and value=category id
    """
    return {c.name: c.id for c in Category.query.all()}
