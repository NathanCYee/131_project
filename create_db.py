import os
from os.path import exists

from sqlalchemy import insert

from app import db

# delete the images
files = os.listdir('./app/static/uploads')
for file in files:
    if ".gitignore" not in file:
        os.remove(os.path.join("./app/static/uploads/", file))

# delete the existing database
if exists('./app/webapp.db'):
    os.remove('./app/webapp.db')
db.create_all()

# construct the roles and categories in the database
from app.models import Role, Category, User, UserRole

cust = Role(name='customer')
merch = Role(name='merchant')
admin = Role(name='admin')
db.session.add(cust)
db.session.add(merch)
db.session.add(admin)

categories = ["Clothing", "Video Games", "Electronics", "Home Decor"]

for category in categories:
    new_cat = Category(name=category)
    db.session.add(new_cat)

db.session.commit()

# Create and register the admin
user = User(username='admin', email='admin@test.com')
user.set_password('password')
db.session.add(user)
db.session.commit()

# assign the merchant role to the user
stmt = insert(UserRole).values(user_id=user.id, role_id=admin.id)
db.session.execute(stmt)
db.session.commit()