"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


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