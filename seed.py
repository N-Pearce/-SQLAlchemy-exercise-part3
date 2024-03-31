"""Seed file for users db"""

from models import User, db
from app import app

# create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

    User.query.delete()

# add users
bob = User(first_name='Bob', last_name='Smith')
allie = User(first_name='Allie', last_name='Brown', image_url='	https://newprofilepic.photo-cdn.net//assets/images/article/profile.jpg?90af0c8')
jonathan = User(first_name='Jonathan', last_name='Mammoth', image_url='https://static-00.iconduck.com/assets.00/profile-default-icon-2048x2045-u3j7s5nj.png')

with app.app_context():
    db.session.add(bob)
    db.session.add(allie)
    db.session.add(jonathan)

    db.session.commit()