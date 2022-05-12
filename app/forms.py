from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.html5 import DateField

from wtforms.validators import DataRequired, Email, Optional, NumberRange
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FloatField, TextAreaField, HiddenField, \
    SelectField, MultipleFileField, SelectMultipleField


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    """The username input of the form"""
    password = PasswordField("Password", validators=[DataRequired()])
    """The password input of the form"""
    submit = SubmitField("Submit")
    """Submit input (should be `True`)"""


class RegisterForm(FlaskForm):
    """
    A form object that receives input for registration of new accounts.
    """
    username = StringField("Username", validators=[DataRequired()])
    """The username input of the form"""
    email = StringField("Email", validators=[DataRequired(), Email()])
    """The email input of the form"""
    password = PasswordField("Password", validators=[DataRequired()])
    """The password input of the form"""
    submit = SubmitField("Submit")
    """Submit input (should be `True`)"""


class PasswordForm(FlaskForm):
    """
    Form object used for password resets
    """
    original_password = PasswordField("Current password", validators=[DataRequired()])
    """The original password of the account"""
    new_password = PasswordField("Password", validators=[DataRequired()])
    """The new choice for password for the account"""
    new_password_repeat = PasswordField("Confirm password", validators=[DataRequired()])
    """A repeated user input for the password"""
    submit = SubmitField("Submit")
    """Submit input (should be `True`)"""


class DeleteAccountForm(FlaskForm):
    """
    Form object used to confirm account deletes
    """
    confirm = BooleanField("I want to delete my account.", validators=[DataRequired()])
    """A boolean input that confirms that the submitter wants their account to be deleted."""
    submit = SubmitField("Delete my account.")
    """Submit input (should be `True`)"""


class ReviewForm(FlaskForm):
    """
    Form object used to add a review to a product
    """
    rating = SelectField("Give a rating from 1 to 5", choices=[i for i in range(1, 6)], default=5,
                         validators=[DataRequired()])
    """A dropdown rating for the user to give a review from 1 to 5"""
    body = TextAreaField("Add a written review")
    """The text body of the review"""
    submit = SubmitField("Submit")
    """Submit input (should be `True`)"""


class CartForm(FlaskForm):
    """
    Form object used to add a product to the user's cart
    """
    product_id = HiddenField("product", validators=[DataRequired()])
    """A hidden field containing the id of the product"""
    quantity = SelectField("Quantity", choices=[i for i in range(1, 11)], default=1, validators=[DataRequired()])
    """The number of the item that the user wants to add to the cart"""
    submit = SubmitField("Add to Cart")
    """Submit input (should be `True`)"""


class CheckoutForm(FlaskForm):
    """
    Form object used to receive order info in order to process the order
    """
    discount_code = HiddenField("Discount")
    """A discount code to apply to the order (optional)."""
    address = StringField("Address", validators=[DataRequired()])
    """The address to ship the order to."""
    billing = StringField("Billing info", validators=[DataRequired()])
    """Credit card information"""
    submit = SubmitField("Place Order")
    """Submit input (should be `True`)"""


class NewProductForm(FlaskForm):
    """
    Form object used to receive input for a new product
    """
    merchant_id = HiddenField("Merchant ID", validators=[DataRequired()])
    """The id of the merchant submitting the new product"""
    name = StringField("Name", validators=[DataRequired()])
    """The name of the product to create"""
    price = FloatField("Price", validators=[DataRequired()])
    """The price of the product"""
    description = TextAreaField("Description")
    """A text description of the product"""
    category = SelectField("Category", default=1)
    """a select field to select the category that the product belongs to"""
    pictures = MultipleFileField("Pictures",
                                 validators=[Optional(),
                                             FileAllowed(['png', 'jpg', 'jpeg', 'webp'], 'Only images are allowed!')])
    """a file upload form that accepts multiple image uploads (png, jpg, jpeg, webp)"""
    submit = SubmitField("Submit")
    """Submit input (should be `True`)"""


class FillOrderForm(FlaskForm):
    """
    Form object used by a merchant to fill orders
    """
    merchant_id = HiddenField("Merchant ID", validators=[DataRequired()])
    """The id of the merchant submitting the order filled request"""
    order_id = HiddenField("Order ID", validators=[DataRequired()])
    """The id of the order that the merchant has filled"""
    submit = SubmitField("Complete")
    """Submit input (should be `True`)"""


class NewDiscountForm(FlaskForm):
    """
    Form object used by a merchant to create a new discount
    """
    code = StringField("Discount Code", validators=[DataRequired()])
    """The code for the new discount"""
    amount = FloatField("Discount Amount", validators=[DataRequired()])
    """The numerical amount of the discount"""
    products = SelectMultipleField("Products", validators=[DataRequired()])
    """A multi-select field containing the products that the discount applies to"""
    expiration_date = DateField("Expiration Date", validators=[DataRequired()])
    """The date when the discount expires"""
    submit = SubmitField("Complete")
    """Submit input (should be `True`)"""

class NewPercentageDiscountForm(FlaskForm):
    """
    Form object used by a merchant to create a new discount
    """
    code = StringField("Discount Code", validators=[DataRequired()])
    """The code for the new discount"""
    amount = FloatField("Discount Amount", validators=[NumberRange(min=1, max=100), DataRequired()])
    """The percentage amount of the discount"""
    products = SelectMultipleField("Products", validators=[DataRequired()])
    """A multi-select field containing the products that the discount applies to"""
    expiration_date = DateField("Expiration Date", validators=[DataRequired()])
    """The date when the discount expires"""
    submit = SubmitField("Complete")
    """Submit input (should be `True`)"""
