from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

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
    
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    
    user = db.relationship('User', backref='posts')
    
    tags = db.relationship('Tag',
                            cascade='all,delete',
                            secondary="posts_tags",
                            backref='tags')
    
    # def __repr__(self):
    #     return f"{self.id} {self.title} user: {self.user_id}"

class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        nullable=False)
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        nullable=False)
    id_combo = db.PrimaryKeyConstraint(post_id, tag_id)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     unique=True)
    
    posts = db.relationship('Post',
                            cascade='all,delete',
                            secondary="posts_tags",
                            backref='posts')
    # posts_tags = db.relationship('PostTag',
    #                              backref='PostTag')
