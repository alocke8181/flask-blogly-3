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

@app.route('/users/new', methods=['GET'])
def new_user_form():
    """Show the New User Form"""
    return render_template('new.html')

@app.route('/users/new', methods=['POST'])
def create_new_user():
    """Create a new user from the form"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None
    
    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
    return redirect('/')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show info for a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('user.html',user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Show the form to edit the user"""
    user = User.query.get(user_id)
    return render_template('edit.html',user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Update the user with new info"""
    user = User.query.get(user_id)
    user.first_name = request.form['new_first_name']
    user.last_name = request.form['new_last_name']
    user.image_url = request.form['new_image_url']

    #with app.app_context():
    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete',methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')
