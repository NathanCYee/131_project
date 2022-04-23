from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

webapp = Flask(__name__)
webapp.static_folder = 'static'

webapp.config.from_mapping(
    SECRET_KEY='you-will-never-guess',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'webapp.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(webapp)

from app import routes
