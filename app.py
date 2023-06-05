"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



connect_db(app)
#db.create_all()

# def create_users():
#     adams = User(first_name='Alex',last_name='Adams',image_url='https://images.generated.photos/3onKkR7UoKpfi_swCssRh9wWxrK_I9jjyc59vM930II/rs:fit:256:256/czM6Ly9pY29uczgu/Z3Bob3Rvcy1wcm9k/LnBob3Rvcy92Ml8w/NjE0ODcxLmpwZw.jpg')
#     bob = User(first_name='Bob',last_name='Roberts')
#     carla = User(first_name='Carla',last_name='Carlyle',image_url='https://images-stylist.s3-eu-west-1.amazonaws.com/app/uploads/2019/04/01103005/tomi-adeyemi-c-elena-seibert-256x256.jpg')
#     users = [adams,bob,carla]
#     with app.app_context():
#         db.session.add_all(users)
#         db.session.commit()

@app.route('/')
def home():
    """Show home page"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('home.html',users=users)
