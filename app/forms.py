from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, Field
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

class CartForm(FlaskForm):
    quantity = StringField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Submit")