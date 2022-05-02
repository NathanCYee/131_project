from itertools import product
from sqlalchemy import insert

from app import webapp, db
from flask import render_template as r, flash, request, redirect, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import CheckoutForm, LoginForm, RegisterForm, PasswordForm, DeleteAccountForm, CartForm, NewProductForm
from app.models import CartItem, Order, OrderRow, Product, User, UserRole, Category
from app.utils import get_merchant, merchant_required, get_category_dict, get_categories


def add_categories(func):
    """Decorator function that automatically adds categories"""

    def inner(*args, **kwargs):
        return func(*args, **kwargs, categories=get_category_dict())

    return inner


render_template = add_categories(r)  # decorate function so that you don't have to manually add categories to each


@webapp.route('/')
def home():
    return render_template('index.html')


@webapp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        users = User.query.filter_by(username=username)
        if users.count() == 0:
            flash("User not found.")
            return render_template('login.html', form=form)
        else:
            user = users.first()
            if user.check_password(password):
                login_user(user)
                return redirect('/', code=302)
            else:  # redirect with an error message
                flash("Incorrect password.")
                return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@webapp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
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
        # create and register the new user
        else:  # redirect with an error message
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
    logout_user()
    return redirect('/')


@webapp.route("/account_info", methods=['GET', 'POST'])
@login_required
def account_info():
    form = PasswordForm()
    if request.method == 'POST' and form.validate():
        password = form.original_password.data
        if current_user.check_password(password):
            if form.new_password.data == form.new_password_repeat.data:  # confirm that the passwords match
                current_user.set_password(form.new_password.data)
                db.session.commit()
                flash("Password successfully changed")
                return render_template('account_info.html', form=form)
            else:
                flash("Passwords do not match")
                return render_template('account_info.html', form=form)
        else:
            flash("Incorrect password. Please enter your original password.")
            return render_template('account_info.html', form=form)
    else:
        return render_template('account_info.html', form=form)


@webapp.route("/delete_account", methods=['GET', 'POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if request.method == 'POST' and form.validate():
        # form.validate should validate confirm as true
        confirm = form.confirm.data
        print(confirm)
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


@webapp.route('/cart', methods=['GET', 'POST'])
@login_required
def add_cart():
    form = CartForm(request.form)
    if request.method == 'POST' and form.validate():
        quantity = form.quantity.data
        prod_id = form.product_id.data
        product_query = Product.query.filter_by(id=prod_id)
        if product_query.count() < 1:
            flash("Product not found!")
            return redirect('/', code=404)
        else:
            product = product_query.first()
            current_rows = current_user.cart_items.filter_by(product_id=product.id)
            if current_rows.count() >= 1:
                row = current_rows.first()
                row.quantity += int(quantity)
                db.session.commit()
            else:
                cart_item = CartItem(product_id=product.id, quantity=quantity, user_id=current_user.id)
                db.session.add(cart_item)
                db.session.commit()
            flash("Item added to cart!")
            return redirect('/cart')
    else:
        cart_items = current_user.cart_items.all()
        rows = {}
        for i, row in enumerate(cart_items):
            product = Product.query.filter_by(id=row.product_id).first()
            rows[i + 1] = {'id': row.id, 'product_name': product.name, 'product_id': product.id,
                           'quantity': row.quantity, 'price': product.price}
        cart = current_user.cart_items.all()
        total = 0
        for i in cart:
            product = Product.query.filter_by(id=i.product_id).first()
            total += (product.price * i.quantity)
        return render_template('cart.html', cart_items=rows, total=total, form=form)


@webapp.route('/cart/remove/<int:row_id>', methods=['GET'])
@login_required
def cart_remove(row_id):
    rows = CartItem.query.filter_by(id=row_id)
    if rows.count() != 1:  # row doesn't exist
        return abort(400)
    else:
        row = rows.first()
        if (row.user_id != current_user.id):  # forbidden, cannot access another user's rows
            return abort(403)
        else:
            product = Product.query.filter_by(id=row.product_id).first()
            name = product.name
            qty = row.quantity
            rows.delete()
            db.session.commit()
            flash(f'Removed {qty} of {name}')
            return redirect('/cart')


@webapp.route('/category/<int:category_id>')
def category(category_id):
    categories = Category.query.filter_by(id=category_id)
    if categories.count() == 1:
        category = categories.first()
        return render_template('category.html', category=category, products=category.products.all())
    else:
        return abort(404)


@webapp.route('/merchant/<int:merchant_id>')
def merchant_profile(merchant_id):
    merchants = User.query.filter(User.roles.any(id=2)).filter_by(id=merchant_id)
    if merchants.count() == 1:
        merchant = merchants.first()
        products = Product.query.filter_by(merchant_id=merchant.id).all()
        return render_template('merchant_profile.html', merchant=merchant, products=products)
    else:
        return abort(404)


@webapp.route('/product/<int:prod_id>')
def product(prod_id):
    form = CartForm(request.form, product_id=prod_id)
    product_match = Product.query.filter_by(id=prod_id)
    if product_match.count() < 1:
        flash('Product not found!')
        return redirect('/', code=302)
    else:
        product = product_match.first()
        merchant = User.query.filter_by(id=product.merchant_id).first()
        return render_template('product.html', product=product, merchant=merchant, form=form)


@webapp.route("/checkout", methods=['GET', 'POST'])
@login_required
def purchase_cart():
    form = CheckoutForm(request.form)
    cart = current_user.cart_items.all()
    total = 0
    for i in cart:
        product = Product.query.filter_by(id=i.product_id).first()
        total += (product.price * i.quantity)
    flash("Total: ", total)
    if request.method == 'POST' and form.validate():
        submit = form.submit.data
        if submit:
            #takes in user info
            address = form.address.data
            billing = form.billing.data
            items = current_user.cart_items()

            #create order
            order = Order(user_id=current_user.id, ship_address=address)
            db.session.add(order)

            rows = OrderRow()
            for row in items: 
                product = Product.query.filter_by(id=row.product_id).first()
                order_row = OrderRow(id=order.id, product_id=row.product_id, quantity=row.quantity,
                                    product_price=product.price)
                db.session.add(order_row)
                db.session.delete(row)

            db.session.commit()
            return render_template('checkout.html', total=total, form=form)
        else:
            flash("You need to confirm to purchase cart")
            return redirect('/checkout')
            


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
    return render_template("merchant_index.html")


@webapp.route('/merchant/register', methods=['GET', 'POST'])
def merchant_register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
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
        # create and register the new user
        else:  # redirect with an error message
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            stmt = insert(UserRole).values(user_id=user.id, role_id=get_merchant().id)
            db.session.execute(stmt)
            db.session.commit()
            login_user(user)
            return redirect('/merchant', code=302)
    else:
        return render_template('merchant_register.html', form=form)


@webapp.route('/merchant/login', methods=['GET', 'POST'])
def merchant_login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        users = User.query.filter(User.roles.any(id=2)).filter_by(username=username)
        if users.count() == 0:
            flash("User not found.")
            return render_template('merchant_login.html', form=form)
        else:
            user = users.first()
            if user.check_password(password):
                login_user(user)
                return redirect('/merchant', code=302)
            else:  # redirect with an error message
                flash("Incorrect password.")
                return render_template('merchant_login.html', form=form)
    else:
        return render_template('merchant_login.html', form=form)


@webapp.route('/merchant/new_product', methods=['GET', 'POST'])
@login_required
@merchant_required
def merchant_new_product():
    form = NewProductForm(request.form, merchant_id=current_user.id)
    form.category.choices = get_categories()
    if request.method == 'POST' and form.validate():
        # TODO: Add categories
        merchant_id = form.merchant_id.data
        name = form.name.data
        price = form.price.data
        description = form.description.data
        category = form.category.data
        category_id = Category.query.filter_by(name=category).first().id
        product = Product(merchant_id=merchant_id, name=name, price=price, description=description,
                          category_id=category_id)
        db.session.add(product)
        db.session.commit()
        return redirect(f'/product/{product.id}', code=302)
    else:
        return render_template('merchant_product.html', form=form, id=current_user.id)
