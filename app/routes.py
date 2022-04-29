from distutils.log import debug
from app import webapp
from flask import render_template, flash

@webapp.route('/')
def home():
    return render_template('home.html')

@webapp.route('/search')
def search():
    return render_template('search.html')

@webapp.route('/checkout')
def cart():
    return render_template('cart.html')
