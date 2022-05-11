import os
from os.path import exists
from app import db

# delete the images
"""files = os.listdir('./app/static/uploads')
for file in files:
    if ".gitignore" not in file:
        os.remove(file)"""

# delete the existing database
if exists('./app/webapp.db'):
    os.remove('./app/webapp.db')
db.create_all()

# construct the roles and categories in the database
from app.models import Role, Category

cust = Role(name='customer')
merch = Role(name='merchant')
db.session.add(cust)
db.session.add(merch)

categories = ["Clothing", "Video Games", "Electronics", "Home Decor"]

for category in categories:
    new_cat = Category(name=category)
    db.session.add(new_cat)

db.session.commit()
