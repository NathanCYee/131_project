from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FloatField, TextAreaField, HiddenField, \
    SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange

from app.models import Product
from app.utils import get_categories


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
    product_id = HiddenField("product", validators=[DataRequired()])
    quantity = SelectField("Quantity", choices=[i for i in range(1, 11)], default=1, validators=[DataRequired()])
    submit = SubmitField("Add to Cart")


class CheckoutForm(FlaskForm):
    confirm = BooleanField("Purchase", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    billing = StringField("Billing info", validators=[DataRequired()])
    submit = SubmitField("Place Order")


class NewProductForm(FlaskForm):
    merchant_id = HiddenField("Merchant ID", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    description = TextAreaField("Description")
    category = SelectField("Category", default=1)
    submit = SubmitField("Submit")
