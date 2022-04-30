from app import webapp, db
from flask import render_template, flash, request, redirect, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm, PasswordForm, DeleteAccountForm
from app.models import User

@webapp.route('/')
def home():
    return render_template('home.html')

@webapp.route('/search')
def search():
    return render_template('search.html')

@webapp.route('/cart')
def cart():
    return render_template('cart.html')

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
    

@webapp.route('/account_test')
@login_required
def account_test():
    """Used for testing, should only be reachable if logged in, else it would redirect the user to the login page"""
    return "You are logged in"
