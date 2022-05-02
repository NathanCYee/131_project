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
    :attr id: The primary key of the role
    :attr name: The name of the role
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class User(UserMixin, db.Model):
    """
    A Model object that represents a user. Also supports UserMixin for FlaskLogin
    :attr id: The primary key of the user
    :attr username: The username of the user
    :attr email: The email of the user
    :attr password_hash: The hashed password of the user
    :attr roles: A queryable database relationship that retrieves the roles related to the user
    :attr cart_items: A queryable relationship that retrieves the rows in the cart related to the customer user
    :attr orders: A queryable relationship that retrieves the orders related to the customer user
    :attr products: A queryable relationship that retrieves the products related to a merchant user
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    # relationships
    roles = db.relationship('Role', secondary='user_role', lazy='dynamic')
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic')
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    products = db.relationship('Product', backref='user', lazy='dynamic')

    def set_password(self, password):
        """
        Sets the password of the given User object
        :param password: The new password to set
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks a password input against the password stored in the User
        :param password: The password to check
        :return: `True` if the passwords match, `False` if not
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Returns a string representation of the User
        :return: A string in the format <User: username email>
        """
        return f'<User: {self.username} {self.email}>'


class Category(db.Model):
    """
    A Model object that represents a category of products
    :attr id: The primary key of the category
    :attr name: The name of the category
    :products: a queryable relationship representing the products that belong to the category
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    products = db.relationship('Product', backref='category', lazy='dynamic')


class Product(db.Model):
    """
    A Model object that represents a product
    :attr id: The primary key of the product
    :attr category_id: The foreign key of the category the product belongs to
    :attr merchant_category: The foreign key of the merchant User the product belongs to
    :attr name: The name of the product
    :attr price: The price of the product
    :attr description: The description of the product
    :attr reviews: A queryable database relationship that retrieves the reviews of the product
    :attr images: A instrumentedList that contains the Image objects related to the product
    :attr orders: A relationship that retrieves orders of the product
    """
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    merchant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(128))
    price = db.Column(db.Float)
    description = db.Column(db.Text)

    # Relationships
    reviews = db.relationship('Review', backref='product', lazy='dynamic')
    images = db.relationship('Image', backref='product')
    orders = db.relationship("OrderRow", back_populates="product")


class Image(db.Model):
    """
    A Model object that contains information about an uploaded image
    :attr id: The primary key of the image
    :attr product_id: The foreign key of which the image is related to
    :attr path: The path to the image
    """
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    path = db.Column(db.String(128))


class CartItem(db.Model):
    """
    A Model object that represents a row in a cart
    :attr id: The primary key of the cart item
    :attr product_id: The foreign key that relates the row to a product
    :attr user_id: The foreign key that relates the row to a customer user
    :attr quantity: The quantity of the product ordered
    :attr timestamp: The time at which the item was created
    """
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quantity = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User ID: {self.user_id} Item: >'


class Order(db.Model):
    """
    A Model object that represents an order
    :attr id: The primary key of the order
    :attr user_id: A foreign key that relates an order to a customer user
    :attr ship_address: The address that the order will be shipped to
    :attr order_row: A queryable relationship that retrieves the OrderRows belonging to an Order
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ship_address = db.Column(db.String(128))
    order_row = db.relationship('OrderRow', backref='order', lazy='dynamic')

    def __repr__(self):
        return f'id: {self.id}\n' \
               f'user_id: {self.user_id}\n' \
               f'ship_address: {self.ship_address}\n' \
               f'order_row: {self.order_row}\n'


class OrderRow(db.Model):
    """
    A Model object that represents a row of an Order
    :attr row_id: The primary key of the order row
    :attr id: A foreign key that relates to the Order that the row belongs to
    :attr product_id: A foreign key that relates to the product purchased in the row
    :attr quantity: The number of the product that was purchased
    :attr product_price: The price of each product at the time it was purchased
    :attr product: A relationship that links to the Product object purchased in the row
    :attr filled: A boolean that represents if the order was filled or not. Defaults to False.
    :attr timestamp: The time at which the OrderRow was created
    """
    row_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    product_price = db.Column(db.Float)
    product = db.relationship("Product", back_populates="orders")
    filled = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'row_id: {self.row_id}\n' \
               f'order id: {self.id}\n' \
               f'product_id: {self.product_id}\n' \
               f'quantity: {self.quantity}\n' \
               f'product_price: {self.product_price}\n'


class Review(db.Model):
    """
    A Model object representing a review
    :attr id: The primary key of the review
    :attr user_id: A foreign key that relates the review to a customer
    :attr product_id: A foreign key that relates the review to a product
    :attr rating: A numerical rating given in the review
    :attr body: The text body of the review
    :attr timestamp: The time at which the review was written
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    rating = db.Column(db.Integer)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        username = User.query.filter_by(id=self.user_id).first().username
        return f'{username}\n' \
               f'{self.rating}\n' \
               f'{self.body}\n'


@login.user_loader
def load_user(id):
    """
    A user loader for flask login
    :param id: The ID of the user to retrieve
    :return: The User object that has the given ID
    """
    return User.query.get(int(id))
