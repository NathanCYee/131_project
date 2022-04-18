from distutils.log import debug
from app import webapp
from flask import render_template, flash

@webapp.route('/')
def home():
    return render_template('base.html')