"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

################################################################################################
class User(db.Model):
    """User"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, default = 'https://winaero.com/blog/wp-content/uploads/2015/05/windows-10-user-account-login-icon.png')

    def full_name(self):
        """Returns the full name of the user"""
        return f'{self.first_name} {self.last_name}'

################################################################################################
class Post(db.Model):
    """Post"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default = datetime.datetime.now)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    owner = db.relationship('User', backref='posts')

    tags = db.relationship('Tag', secondary='post_tag', backref='posts')

################################################################################################
class Tag(db.Model):
    """Tag"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, unique=True, nullable=False)

################################################################################################
class PostTag(db.Model):
    """Relationship Table b/w Post and Tag"""

    __tablename__ = 'post_tag'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True )

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)