from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, HiddenField, SelectField, \
    MultipleFileField, DecimalField
from wtforms.validators import DataRequired, Email, Optional
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FloatField, TextAreaField, HiddenField, \
    SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange


class LoginForm(FlaskForm):
    """
    A form object that receives input for logins.
    :attr username: The username input of the form
    :attr password: The password input of the form
    :attr submit: Submit input (should be True)
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    """
    A form object that receives input for registration of new accounts.
    :attr username: The username input of the form
    :attr email: The email input of the form
    :attr password: The password input of the form
    :attr submit: Submit input (should be True)
    """
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    """
    Form object used for password resets
    :attr original_password: The original password of the account
    :attr new_password: The new choice for password for the account
    :attr new_password_repeat: A repeated user input for the password
    """
    original_password = PasswordField("Current password", validators=[DataRequired()])
    new_password = PasswordField("Password", validators=[DataRequired()])
    new_password_repeat = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class DeleteAccountForm(FlaskForm):
    """
    Form object used to confirm account deletes
    :attr confirm: A boolean input that confirms that the submitter wants their account to be deleted if true
    :attr submit: Submit input (should be True)
    """
    confirm = BooleanField("I want to delete my account.", validators=[DataRequired()])
    submit = SubmitField("Delete my account.")


class ReviewForm(FlaskForm):
    """
    Form object used to add a review to a product
    :attr rating: A dropdown rating for the user to give a review from 1 to 5
    :attr body: The text body of the review
    :attr submit: Submit input (should be True)
    """
    rating = SelectField("Give a rating from 1 to 5", choices=[i for i in range(1, 6)], default=5,
                         validators=[NumberRange(1, 5, "1-5"), DataRequired()])
    body = TextAreaField("Add a written review")
    submit = SubmitField("Submit")


class CartForm(FlaskForm):
    """
    Form object used to add a product to the user's cart
    :attr product_id: A hidden field containing the id of the product
    :attr quantity: The number of the item that the user wants to add to the cart
    :attr submit: Submit input (should be True)
    """
    product_id = HiddenField("product", validators=[DataRequired()])
    quantity = SelectField("Quantity", choices=[i for i in range(1, 11)], default=1, validators=[DataRequired()])
    submit = SubmitField("Add to Cart")


class CheckoutForm(FlaskForm):
    """
    Form object used to receive order info in order to process the order
    :attr address: The address to ship the order to.
    :attr billing: Credit card information
    :attr submit: Submit input (should be True)
    """
    address = StringField("Address", validators=[DataRequired()])
    billing = StringField("Billing info", validators=[DataRequired()])
    submit = SubmitField("Place Order")


class NewProductForm(FlaskForm):
    """
    Form object used to receive input for a new product
    :attr merchant_id: The id of the merchant submitting the new product
    :attr name: The name of the product to create
    :attr price: The price of the product (float)
    :attr description: A text description of the product
    :attr category: a select field to select the category that the product belongs to
    :att pictures: a file upload form that accepts multiple image uploads (png, jpg, jpeg, webp)
    :attr submit: Submit input (should be True)
    """
    merchant_id = HiddenField("Merchant ID", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    description = TextAreaField("Description")
    category = SelectField("Category", default=1)
    pictures = MultipleFileField("Pictures",
                                 validators=[Optional(),
                                             FileAllowed(['png', 'jpg', 'jpeg', 'webp'], 'Only images are allowed!')])
    submit = SubmitField("Submit")


class FillOrderForm(FlaskForm):
    """
    Form object used by a merchant to fill orders
    :attr merchant_id: The id of the merchant submitting the order filled request
    :attr order_id: the id of the order that the merchant has filled
    :attr submit: Submit input (should be True)
    """
    merchant_id = HiddenField("Merchant ID", validators=[DataRequired()])
    order_id = HiddenField("Order ID", validators=[DataRequired()])
    submit = SubmitField("Complete")
