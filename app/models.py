from datetime import datetime

from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

UserRole = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(db.Model):
    """
    An Model object that contains the name of a role
    """
    id = db.Column(db.Integer, primary_key=True)
    """The primary key of the role"""
    name = db.Column(db.String(255), nullable=False, unique=True)
    """The name of the role"""


class User(UserMixin, db.Model):
    """
    A Model object that represents a user. Also supports UserMixin for FlaskLogin
    """
    id = db.Column(db.Integer, primary_key=True)
    """The primary key of the user"""
    username = db.Column(db.String(64), unique=True)
    """The username of the user"""
    email = db.Column(db.String(64), unique=True)
    """The email of the user"""
    password_hash = db.Column(db.String(128))
    """The hashed password of the user"""

    # relationships
    roles = db.relationship('Role', secondary='user_role', lazy='dynamic')
    """A queryable database relationship that retrieves the roles related to the user"""
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic')
    """A queryable relationship that retrieves the rows in the cart related to the customer user"""
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    """A queryable relationship that retrieves the orders related to the customer user"""
    products = db.relationship('Product', backref='user', lazy='dynamic')
    """A queryable relationship that retrieves the products related to a merchant user"""

    def set_password(self, password):
        """
        Sets the password of the given User object

        :param str password: The new password to set
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks a password input against the password stored in the User

        :param str password: The password to check
        :return: `True` if the passwords match, `False` if not
        :rtype: bool
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Returns a string representation of the User

        :return: A string in the format <User: username email>
        :rtype: str
        """
        return f'<User: {self.username} {self.email}>'


class Category(db.Model):
    """
    A Model object that represents a category of products
    """
    id = db.Column(db.Integer, primary_key=True)
    """The primary key of the category"""
    name = db.Column(db.String(128))
    """The name of the category"""
    products = db.relationship('Product', backref='category', lazy='dynamic')
    """A queryable relationship representing the products that belong to the category"""


class Product(db.Model):
    """
    A Model object that represents a product
    """
    id = db.Column(db.Integer, primary_key=True)
    """The primary key of the product"""
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    """The foreign key of the category the product belongs to"""
    merchant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """The foreign key of the merchant User the product belongs to"""
    name = db.Column(db.String(128))
    """The name of the product"""
    price = db.Column(db.Float)
    """The price of the product"""
    description = db.Column(db.Text)
    """The description of the product"""

    # Relationships
    reviews = db.relationship('Review', backref='product', lazy='dynamic')
    """A queryable database relationship that retrieves the reviews of the product"""
    images = db.relationship('Image', backref='product')
    """A instrumentedList that contains the Image objects related to the product"""
    orders = db.relationship("OrderRow", back_populates="product")
    """A relationship that retrieves orders of the product"""


class Image(db.Model):
    """
    A Model object that contains information about an uploaded image
    """
    id = db.Column(db.Integer, primary_key=True)
    """The primary key of the image"""
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    """The foreign key of which the image is related to"""
    path = db.Column(db.String(128))
    """The path to the image"""


class CartItem(db.Model):
    """
    A Model object that represents a row in a cart
    """
    id = db.Column(db.Integer, primary_key=True)
    """The primary key of the cart item"""
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    """The foreign key that relates the row to a product"""
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """The foreign key that relates the row to a customer user"""
    quantity = db.Column(db.Integer)
    """The quantity of the product ordered"""
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    """The time at which the item was created"""

    def __repr__(self):
        return f'<User ID: {self.user_id} Item: >'


class Order(db.Model):
    """
    A Model object that represents an order
    """
    id = db.Column(db.Integer, primary_key=True)
    """The primary key of the order"""
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """A foreign key that relates an order to a customer user"""
    ship_address = db.Column(db.String(128))
    """The address that the order will be shipped to"""
    order_row = db.relationship('OrderRow', backref='order', lazy='dynamic')
    """A queryable relationship that retrieves the OrderRows belonging to an Order"""

    def __repr__(self):
        return f'id: {self.id}\n' \
               f'user_id: {self.user_id}\n' \
               f'ship_address: {self.ship_address}\n' \
               f'order_row: {self.order_row}\n'


class OrderRow(db.Model):
    """
    A Model object that represents a row of an Order
    """
    row_id = db.Column(db.Integer, primary_key=True)
    """The primary key of the order row"""
    id = db.Column(db.Integer, db.ForeignKey('order.id'))
    """A foreign key that relates to the Order that the row belongs to"""
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    """A foreign key that relates to the product purchased in the row"""
    quantity = db.Column(db.Integer)
    """The number of the product that was purchased"""
    product_price = db.Column(db.Float)
    """The price of each product at the time it was purchased"""
    product = db.relationship("Product", back_populates="orders")
    """A relationship that links to the Product object purchased in the row"""
    filled = db.Column(db.Boolean, default=False)
    """A boolean that represents if the order was filled or not. Defaults to `False`."""
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    """The time at which the OrderRow was created. Defaults to `datetime.utcnow`."""

    def __repr__(self):
        return f'row_id: {self.row_id}\n' \
               f'order id: {self.id}\n' \
               f'product_id: {self.product_id}\n' \
               f'quantity: {self.quantity}\n' \
               f'product_price: {self.product_price}\n'


class Review(db.Model):
    """
    A Model object representing a review
    """
    id = db.Column(db.Integer, primary_key=True)
    """The primary key of the review"""
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """A foreign key that relates the review to a customer"""
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    """A foreign key that relates the review to a product"""
    rating = db.Column(db.Integer)
    """A numerical rating given in the review"""
    body = db.Column(db.Text)
    """The text body of the review"""
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    """The time at which the review was written. Defaults to `datetime.utcnow`."""

    def __repr__(self):
        username = User.query.filter_by(id=self.user_id).first().username
        return f'{username}\n' \
               f'{self.rating}\n' \
               f'{self.body}\n'


class Discount(db.Model):
    """
    A Model object that represents a user. Also supports UserMixin for FlaskLogin. Construct a discount using the
    ``app.utils.create_discount`` method.
    """
    id = db.Column(db.Integer, primary_key=True)
    """The primary key of the discount"""
    code = db.Column(db.String(64), nullable=False, unique=True)
    """The code of the discount that the user can use"""
    expiration = db.Column(db.DateTime)
    """The expiration date of the discount"""
    details = db.Column(db.JSON, nullable=False)
    """A JSON attribute containing the details of the discount"""

    def is_valid(self):
        """
        Compares the current datetime to the stored expiration date to confirm if the discount is still valid

        :return: `True` if the current date is on or before the expiration date. `False` if it is after.
        :rtype: bool
        """
        cur_date = datetime.today()
        return cur_date <= self.expiration

    def apply_discount(self, cart_item: int):
        """
        Returns the discount amount for a given ``app.models.CartItem`` row id.

        :param cart_item: The id field of the ``app.models.CartItem``
        :return: The discount amount for the given row.
        :rtype: float
        """
        row = CartItem.query.get(cart_item)
        if self.is_valid() and row is not None:
            discount_details = self.details
            product = Product.query.get(row.product_id)
            if discount_details['type'] == 2:
                if discount_details['percentage']:
                    discount = discount_details['amount'] * product.price
                    return discount
                if not discount_details['percentage']:
                    return discount_details['amount']
            if discount_details['type'] == 1 and product.category_id in discount_details["applicable_id"]:
                if discount_details['percentage']:
                    discount = discount_details['amount'] * product.price
                    return discount
                if not discount_details['percentage']:
                    return discount_details['amount']
            if discount_details['type'] == 0 and product.id in discount_details["applicable_id"]:
                if discount_details['percentage']:
                    discount = discount_details['amount'] * product.price
                    return discount
                if not discount_details['percentage']:
                    return discount_details['amount']
            return 0
        return 0


@login.user_loader
def load_user(id):
    """
    A user loader for flask login

    :param id: The ID of the user to retrieve
    :return: The User object that has the given ID
    :rtype: app.models.User
    """
    return User.query.get(int(id))
