from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FloatField, TextAreaField, HiddenField, \
    SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange


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


class ReviewForm(FlaskForm):
    rating = IntegerField("Give a rating from 1 to 5", validators=[NumberRange(1, 5, "1-5"),
                                                                   DataRequired()])
    body = TextAreaField("Add a written review")
    submit = SubmitField("Submit")


class CartForm(FlaskForm):
    product_id = HiddenField("product", validators=[DataRequired()])
    quantity = SelectField("Quantity", choices=[i for i in range(1, 11)], default=1, validators=[DataRequired()])
    submit = SubmitField("Add to Cart")


class CheckoutForm(FlaskForm):
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
