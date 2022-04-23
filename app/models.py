from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

"""class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post')#, backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User: {self.username} {self.email}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body= db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<User ID: {self.user_id} {self.body}>'
"""


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User: {self.username} {self.email}>'
