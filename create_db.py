import os
from os.path import exists
from app import db

if exists('./app/webapp.db'):
    os.remove('./app/webapp.db')
db.create_all()

from app.models import Role, Category

cust = Role(name='customer')
merch = Role(name='merchant')
db.session.add(cust)
db.session.add(merch)

categories = ["Clothing", "Video Games", "Electronics"]

for category in categories:
    new_cat = Category(name=category)
    db.session.add(new_cat)

db.session.commit()
