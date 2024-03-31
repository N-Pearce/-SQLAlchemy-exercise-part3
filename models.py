from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)
    image_url = db.Column(db.Text,
                          default='https://static-00.iconduck.com/assets.00/profile-default-icon-2048x2045-u3j7s5nj.png')
    
    def __repr__(self):
        u = self
        return f"<User id={u.id} name={u.first_name} {u.last_name} image_url={u.image_url}"