from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    original_password = PasswordField("Current password", validators=[DataRequired()])
    new_password = PasswordField("Password", validators=[DataRequired()])
    new_password_repeat = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class DeleteAccountForm(FlaskForm):
    confirm = BooleanField("I want to delete my account.", validators=[DataRequired()])
    submit = SubmitField("Delete my account.")

class CartForm(FlaskForm):
    quantity = StringField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Submit")