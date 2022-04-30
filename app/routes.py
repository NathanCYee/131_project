import os
import uuid

from sqlalchemy import insert, select
from werkzeug.utils import secure_filename

from flask import render_template as r, flash, request, redirect, abort, url_for, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from app import webapp, db
from app.models import User, UserRole, Product, Category, Image, OrderRow, Order
from app.forms import LoginForm, RegisterForm, PasswordForm, DeleteAccountForm, NewProductForm, FillOrderForm
from app.utils import get_merchant, merchant_required, get_category_dict, get_categories, prevent_merchant


def add_categories(func):
    """Decorator function that automatically adds categories to render_template"""

    def inner(*args, **kwargs):
        return func(*args, **kwargs, categories=get_category_dict())

    return inner


render_template = add_categories(r)  # decorate function so that you don't have to manually add categories to each


@webapp.route('/')
@prevent_merchant
def home():
    """Returns the home page of the website to the user. Allows non-logged in users and customer users to access."""
    return render_template('index.html')


@webapp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Return a site that takes user input for login/password to login to an account. Will verify login information if
    accessed through a POST request.
    """
    form = LoginForm(request.form)
    # validate the login
    if request.method == 'POST' and form.validate():
        # retrieve form params
        username = form.username.data
        password = form.password.data

        # search for the username in the table
        users = User.query.filter_by(username=username)
        if users.count() == 0:  # no users with the matching username
            flash("User not found.")
            return render_template('login.html', form=form)
        else:
            # grab the first User object and check
            user = users.first()
            if user.check_password(password):
                login_user(user)
                return redirect('/', code=302)
            else:  # redirect with an error message
                flash("Incorrect password.")
                return render_template('login.html', form=form)
    else:
        # return the login form
        return render_template('login.html', form=form)


@webapp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Return a site that takes user input to create a new customer account. Will verify registration information if
    accessed through a POST request.
    """
    form = RegisterForm(request.form)

    # validate the registration
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # query for the username and check if it is already taken
        if User.query.filter_by(username=username).count() != 0:
            flash("Username is already taken")
            return render_template('register.html', form=form)
        # query for the email and check if it is already taken
        elif User.query.filter_by(email=email).count() != 0:
            flash("Email has already been used")
            return render_template('register.html', form=form)
        else:
            # create and register the new user
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect('/', code=302)
    else:
        return render_template('register.html', form=form)


@webapp.route("/logout")
@login_required
def logout():
    """Logs out the user using flask-login when accessed."""
    logout_user()
    return redirect('/')


@webapp.route("/account_info", methods=['GET', 'POST'])
@login_required
def account_info():
    """
    Returns a page containing information about the username and email as well as a form to change the password.
    When accessed through POST, will validate and process the password change form.
    """
    form = PasswordForm(request.form)

    # process the password change form
    if request.method == 'POST' and form.validate():

        password = form.original_password.data

        # ensure that the password matches the current user
        if current_user.check_password(password):
            # confirm that the passwords match
            if form.new_password.data == form.new_password_repeat.data:
                # change the password and update
                current_user.set_password(form.new_password.data)
                db.session.commit()
                flash("Password successfully changed")
                return render_template('account_info.html', form=form)
            else:
                # new password selection was wrong
                flash("Passwords do not match")
                return render_template('account_info.html', form=form)
        else:
            # original password was wrong, abort password change
            flash("Incorrect password. Please enter your original password.")
            return render_template('account_info.html', form=form)
    else:
        return render_template('account_info.html', form=form)


@webapp.route("/delete_account", methods=['GET', 'POST'])
@login_required
def delete_account():
    """
    Contains a form for the user to confirm that they want to delete their account. When submitted through POST, will
    receive and validate the request before deleting the account from the database.
    """
    form = DeleteAccountForm(request.form)

    # Process the delete account form
    if request.method == 'POST' and form.validate():
        # form.validate should validate confirm as true
        confirm = form.confirm.data

        # delete the account
        if confirm:
            User.query.filter_by(id=current_user.id).delete()
            db.session.commit()
            flash("Account successfully deleted")
            return redirect('/logout')
        else:
            # form should only be submittable if true, this data should never be reached
            return abort(403, "Invalid form data received")
    else:
        return render_template('delete_account.html', form=form)


@webapp.route('/product/<int:prod_id>')
def product(prod_id):
    """
    Retrieve a product page for a given product id. Will abort with a 404 if the ID was not found.
    :param prod_id: The id of the Product to retrieve
    """

    # query the database for the id
    product_match = Product.query.filter_by(id=prod_id)
    if product_match.count() < 1:
        # product id was not found
        return abort(404)
    else:
        # retrieve the first object from the query
        product = product_match.first()
        # get the merchant of the product
        merchant = User.query.filter_by(id=product.merchant_id).first()
        return render_template('product.html', product=product, merchant=merchant)


@webapp.route('/search', methods=['GET'])
@webapp.route('/search/', methods=['GET'])
def search():
    """
    Returns a page with search results from a regex search using the param q as the query from a get request.
    """

    # retrieve the query string from the URL arguments
    form_query = request.args.get('q')

    # check if a value was inputted and not empty
    if form_query is not None and len(form_query) != 0:
        # use regex match on the regex expression to find results
        results = Product.query.where(Product.name.regexp_match(form_query)).all()
        # display search page
        return render_template("search.html", products=results, query=form_query)
    else:
        # invalid search
        return redirect('/')


@webapp.route('/orders')
@login_required
@prevent_merchant
def orders():
    """
    Returns a page to a logged in customer user containing orders with unfilled rows. Redirects if logged in as a
    merchant or not logged in.
    """

    # retrieve the order rows that belong to the customer
    rows = Order.query.filter_by(user_id=current_user.id).all()

    # build a dictionary to send to Jinja
    items = {}
    for order in rows:
        # grab the rows belonging to the order which are not filled
        order_rows = order.order_row.filter_by(filled=False).all()
        for o in order_rows:
            # add the new row to the dictionary if not present
            if order.id not in items:
                items[order.id] = {'order': order, 'rows': [(o, o.product)]}
            else:
                # modify an existing entry in the dictionary
                items[order.id]['rows'].append((o, o.product))
    return render_template('orders.html', orders=items)


@webapp.route('/orders/filled')
@login_required
@prevent_merchant
def orders_filled():
    """
    Returns a page to a logged in customer user containing orders with filled rows. Redirects if logged in as a
    merchant or not logged in.
    """

    # retrieve the order rows that belong to the customer
    rows = Order.query.filter_by(user_id=current_user.id).all()

    # build a dictionary to send to Jinja
    items = {}
    for order in rows:
        # grab the rows belonging to the order which are not filled
        order_rows = order.order_row.filter_by(filled=True).all()
        for o in order_rows:
            # add the new row to the dictionary if not present
            if order.id not in items:
                items[order.id] = {'order': order, 'rows': [(o, o.product)]}
            else:
                # modify an existing entry in the dictionary
                items[order.id]['rows'].append((o, o.product))
    return render_template('orders_filled.html', orders=items)


@webapp.route('/account_test')
@login_required
def account_test():
    """Used for testing, should only be reachable if logged in, else it would redirect the user to the login page"""
    return "You are logged in"


@webapp.route('/merchant/account_test')
@login_required
@merchant_required
def merchant_account_test():
    """Used for testing, should only be reachable if logged in as a merchant, else it would redirect the user to the
    login page"""
    return "You are logged in as a merchant"


@webapp.route('/merchant')
@login_required
@merchant_required
def merchant():
    """Returns a home page for a user logged in as a merchant. Redirects if not logged in as a merchant."""
    return render_template("merchant_index.html")


@webapp.route('/merchant/register', methods=['GET', 'POST'])
def merchant_register():
    """
    Return a site that takes user input to create a new merchant account. Will verify registration information if
    accessed through a POST request.
    """
    form = RegisterForm(request.form)

    # verify a registration
    if request.method == 'POST' and form.validate():
        # retrieve form data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # query for the username and check if it is already taken
        if User.query.filter_by(username=username).count() != 0:
            flash("Username is already taken")
            return render_template('merchant_register.html', form=form)
        # query for the email and check if it is already taken
        elif User.query.filter_by(email=email).count() != 0:
            flash("Email has already been used")
            return render_template('merchant_register.html', form=form)
        else:
            # create and register the new user
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            # assign the merchant role to the user
            stmt = insert(UserRole).values(user_id=user.id, role_id=get_merchant().id)
            db.session.execute(stmt)
            db.session.commit()

            # log the user into their account
            login_user(user)
            return redirect('/merchant', code=302)
    else:
        return render_template('merchant_register.html', form=form)


@webapp.route('/merchant/login', methods=['GET', 'POST'])
def merchant_login():
    """
    Return a site that takes user input for login/password to log in to a merchant account. Will verify login
    information if accessed through a POST request.
    """
    form = LoginForm(request.form)

    # verify a login
    if request.method == 'POST' and form.validate():
        # retrieve form input
        username = form.username.data
        password = form.password.data

        # search for the username in users with merchant role
        users = User.query.filter(User.roles.any(id=get_merchant().id)).filter_by(username=username)
        if users.count() == 0:
            flash("User not found.")
            return render_template('merchant_login.html', form=form)
        else:
            user = users.first()  # grab the first match
            # validate login
            if user.check_password(password):
                # successful login as a merchant
                login_user(user)
                return redirect('/merchant', code=302)
            else:
                # redirect with an error message
                flash("Incorrect password.")
                return render_template('merchant_login.html', form=form)
    else:
        return render_template('merchant_login.html', form=form)


@webapp.route('/merchant/new_product', methods=['GET', 'POST'])
@merchant_required
@login_required
def merchant_new_product():
    """
    Returns a merchant input to submit a new product. When accessed through a POST request, will save inputs, create
    a new Product object, and redirect the user to the product page once submitted.
    """

    # create the form
    form = NewProductForm(request.form, merchant_id=current_user.id)
    form.category.choices = get_categories()  # set the choices as a list of available categories in the database

    # validate the submission
    if request.method == 'POST' and form.validate():
        # retrieve the information about the product
        merchant_id = form.merchant_id.data
        name = form.name.data
        price = form.price.data
        description = form.description.data
        category = form.category.data

        # fetch the category that the product belongs to
        category_id = Category.query.filter_by(name=category).first().id

        # save the new product to the database
        product = Product(merchant_id=merchant_id, name=name, price=price, description=description,
                          category_id=category_id)
        db.session.add(product)
        db.session.commit()

        # Retrieve files sent in the request
        files = request.files.getlist(form.pictures.name)
        if len(files) != 0 and files[0].filename != '':  # check if there are files and the file name is not blank
            for file in files:
                # generate a secure and random filename for the file
                filename = secure_filename(str(uuid.uuid4()) + '.' + file.filename.split('.')[1])
                # save the file to the upload folder
                file.save(os.path.join(webapp.config['UPLOAD_FOLDER'], filename))
                # generate an image and attach it to the product
                route = Image(product_id=product.id, path=url_for('images', name=filename))
                db.session.add(route)
        db.session.commit()

        return redirect(f'/product/{product.id}', code=302)
    else:
        return render_template('merchant_product.html', form=form, id=current_user.id)


@webapp.route('/merchant/orders', methods=['GET', 'POST'])
@merchant_required
@login_required
def merchant_orders():
    """
    Return a site with unfilled orders for a logged-in merchant. When accessed with a POST request with the correct form,
    will change the status of the order rows to filled.
    """
    form = FillOrderForm(request.form)

    # validate a order fill form
    if request.method == 'POST' and form.validate():
        # get data from the form
        order_id = form.order_id.data
        merchant_id = form.merchant_id.data

        # select rows that belong to the merchant
        query = select(OrderRow, Product).join(Product.orders).where(OrderRow.filled == False) \
            .where(OrderRow.id == order_id).where(Product.merchant_id == merchant_id)
        rows = db.session.execute(query).all()

        # loop through and fill the orders
        for order, _ in rows:
            order.filled = True
        db.session.commit()
        return redirect('/merchant/orders')
    else:
        # select all unfilled orders that belong to the merchant
        query = select(OrderRow, Product).join(Product.orders).where(OrderRow.filled == False). \
            where(Product.merchant_id == current_user.id)
        results = db.session.execute(query.order_by(OrderRow.timestamp)).all()

        # build a dictionary to group together orders
        items = {}
        for order, product in results:
            total_order = Order.query.filter_by(id=order.id).first()
            if order.id not in items:
                items[order.id] = {'order': total_order, 'rows': [(order, product)]}
            else:
                items[order.id]['rows'].append((order, product))
        return render_template('merchant_orders.html', orders=items, form=form, id=current_user.id)


@webapp.route('/merchant/orders/filled')
@merchant_required
@login_required
def merchant_orders_filled():
    """
    Return a site with filled orders for a logged-in merchant.
    """

    # select all filled orders that belong to the merchant
    query = select(OrderRow, Product).join(Product.orders).where(OrderRow.filled == True). \
        where(Product.merchant_id == current_user.id)
    results = db.session.execute(query.order_by(OrderRow.timestamp)).all()

    # build a dictionary to group together orders
    items = {}
    for order, product in results:
        total_order = Order.query.filter_by(id=order.id).first()
        if order.id not in items:
            items[order.id] = {'order': total_order, 'rows': [(order, product)]}
        else:
            items[order.id]['rows'].append((order, product))
    return render_template('merchant_orders_filled.html', orders=items)


@webapp.route('/images/<string:filename>')
@webapp.route('/images/<string:filename>/')
def images(filename):
    """
    Retrieves an uploaded file
    :param filename: The name of the file
    :return: an image (.png, .jpg, .jpeg) that was uploaded
    """
    return send_from_directory(webapp.config["UPLOAD_FOLDER"], filename)
