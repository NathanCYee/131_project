from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FloatField, TextAreaField, HiddenField, \
    SelectField, MultipleFileField
from wtforms.validators import DataRequired, Email


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


class NewProductForm(FlaskForm):
    """
    Form object used to receive input
    """
    merchant_id = HiddenField("Merchant ID", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    description = TextAreaField("Description")
    category = SelectField("Category", default=1)
    pictures = MultipleFileField("Pictures",
                                 validators=[FileAllowed(['png', 'jpg', 'jpeg'], 'Only images are allowed!')])
    submit = SubmitField("Submit")
