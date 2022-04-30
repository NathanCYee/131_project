from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
content_folder = os.path.join(basedir, 'static/uploads')

webapp = Flask(__name__)
webapp.static_folder = 'static'
webapp.add_url_rule(
    "/images/<name>", endpoint="images", build_only=True
)

webapp.config.from_mapping(
    SECRET_KEY='you-will-never-guess',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'webapp.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    UPLOAD_FOLDER=content_folder,
    MAX_CONTENT_LENGTH=4 * 1024 ** 2  # 4MB
)

db = SQLAlchemy(webapp)
login = LoginManager(webapp)
login.login_view = 'login'

from app import routes
