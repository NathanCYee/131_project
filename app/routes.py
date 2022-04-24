from app import webapp, db
from flask import render_template, flash, request, redirect
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm
from app.models import User


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
