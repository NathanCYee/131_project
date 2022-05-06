# E-Buy

[![CircleCI](https://circleci.com/gh/NathanCYee/131_project/tree/master.svg?style=svg)](https://circleci.com/gh/NathanCYee/131_project/tree/master)
[![codecov](https://codecov.io/gh/NathanCYee/131_project/branch/master/graph/badge.svg?token=G6YR4ZSL9J)](https://codecov.io/gh/NathanCYee/131_project)
[![Last Commit](https://img.shields.io/github/last-commit/NathanCYee/131_project)](https://github.com/NathanCYee/131_project/commits/)
![Built by SJSU Students](https://badgen.net/badge/Built%20by/SJSU%20Students/yellow)
[![Trello](https://img.shields.io/badge/Trello-%23026AA7.svg?style=flat&logo=Trello&logoColor=white)
](https://trello.com/b/1UQLG3ci/team-13)

E-Buy is a revolutionary E-Commerce website that connects merchants with customers.

## Table of Contents

- [Features](https://github.com/NathanCYee/131_project#Features)
- [Setup and Install](https://github.com/NathanCYee/131_project#Setup-and-Install)
- [Technologies](https://github.com/NathanCYee/131_project#Technologies)
- [Team Members](https://github.com/NathanCYee/131_project#Team-Members)
- [Team Progress](https://github.com/NathanCYee/131_project#Team-Progress)

## Features

- Login and register account functionality accessible through `/login` and `/register`
- Account information, delete account, and change password accessible through `/account_info`
- Previous orders for customers accessible through `/orders`
- Merchant portal accessible through `/merchant`
    - Merchant login/register accessible through `/merchant/login` and `/merchant/register`
    - Create a new product accessible through `/merchant/new_product`
        - Merchants can view and fill orders through `/merchant/orders`
- Product pages with the url `/product/<id>`
    - Add to cart functionality with quantity on product pages
    - Product reviews for customers that have ordered a product
    - Displays product images uploaded by merchant
- Product catalogs with the url `/catalog/<id>`
- Merchant catalog accessible through `/merchant/<id>`
- REGEX search accessible through search form in the navbar
- Cart located at `/cart` for logged-in users
- Checkout cart link located in the cart

## Setup and Install

Please make sure python 3 is installed (working on python 3.8).

- Download the library as a zip or by cloning it using `git clone https://github.com/NathanCYee/131_project.git`
- Navigate to the folder in which the project is stored (e.g. `cd 131_project`)
- Install the prerequisites using `pip install .`
- Setup and create the database by running the create_db.py file using ``python3 create_db.py``
- Run the webapp by running `python3 run.py`
- If run on a local machine, site will be accessible at `localhost:5000` or `http://127.0.0.1:5000/` from a browser

If errors occur with jinja, try to manually upgrade flask by using `pip install --upgrade Flask`.

## Technologies

Project was built with:

- Python 3.8
    - [Flask](https://github.com/pallets/flask) - Web framework for python
    - [Flask-SQLAlchemy](https://github.com/pallets-eco/flask-sqlalchemy) - ORM for SQL databases that connects with
      Flask
    - [Flask-login](https://github.com/maxcountryman/flask-login) - User session management (login/logout) for flask
    - [flask-wtf](https://github.com/wtforms/flask-wtf) - Form creation, validation, and management for Flask
    - [Pytest](https://github.com/pytest-dev/pytest) - Unit testing library for python
- [Bootstrap](https://github.com/twbs/bootstrap) - Web component library
    - [Bootstrap Icons](https://github.com/twbs/icons) - Icons provided by bootstrap
    - [vinorodrigues/bootstrap-dark-5](https://github.com/vinorodrigues/bootstrap-dark-5) - Toggleable dark mode for
      bootstrap
- [CircleCI](https://circleci.com/) - Continuous integration/deployment
- [Codecov](https://about.codecov.io/) - Code coverage metrics

## Team Progress

- [Gantt Chart](https://docs.google.com/spreadsheets/d/1MNufmraxPGaFWcTLx7IgA9EN_BQ6yrKa3Abu86le8Vo/edit?usp=sharing) -
  Chart to track team's progress on development
- [Documentation](https://nathancyee.github.io/131_project/) - Code documentation for the app package.

## Team Members

- Sarah Singh-**LEAD** ([@SarahS16](https://github.com/SarahS16))
- Selim Ishakbeyoglu ([@SelimIshakb](https://github.com/SelimIshakb))
- Nicholas ([@StickOnAStick](https://github.com/StickOnAStick))
- Nathan Yee ([@NathanCYee](https://github.com/NathanCYee))

---
![Your Repository's Stats](https://contrib.rocks/image?repo=NathanCYee/131_project)