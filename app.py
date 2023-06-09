"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



connect_db(app)
#db.create_all()

@app.route('/')
def home():
    """Show home page"""
    users = User.query.order_by(User.last_name, User.first_name).limit(3).all()
    posts = Post.query.order_by(Post.created_at).limit(3).all()
    tags = Tag.query.order_by(Tag.name).limit(3).all()
    return render_template('home.html',users=users, posts=posts, tags=tags)

################################################################################################
#User related routes

@app.route('/users')
def show_all_users():
    """Show all users"""
    users = User.query.all()
    return render_template('user/users.html', users=users)

@app.route('/users/new', methods=['GET'])
def new_user_form():
    """Show the New User Form"""
    return render_template('user/new_user.html')

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
    return render_template('user/user.html',user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Show the form to edit the user"""
    user = User.query.get(user_id)
    return render_template('user/edit_user.html',user=user)

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

################################################################################################
#Post related routes

@app.route('/posts')
def show_all_posts():
    """Show all posts"""
    posts = Post.query.all()
    return render_template('post/posts.html', posts= posts)

@app.route('/users/<int:user_id>/posts/new',methods=['GET'])
def show_new_post_form(user_id):
    """Show the new post form"""
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template('post/new_post.html',user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new',methods=['POST'])
def new_post(user_id):
    """Create a new post"""
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist('tag')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title, content=content, owner_id=user_id, tags=tags)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/posts/{new_post.id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show the post"""
    post = Post.query.get(post_id)
    return render_template('post/post.html',post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def show_edit_post(post_id):
    """Show the edit post form"""
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    return render_template('post/edit_post.html',post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Edit the post in the db"""
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist('tag')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit() 
    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete the post"""
    post = Post.query.get(post_id)
    owner_id = post.owner_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{owner_id}')

################################################################################################
#Tag related routes

@app.route('/tags')
def show_tags():
    """Show a list of all tags"""
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tag/tags.html', tags=tags)


@app.route('/tags/new', methods=['GET'])
def show_new_tag():
    """Show the form to make a new tag"""
    return render_template('tag/new_tag.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    """Add new tag to db"""
    tag_name = request.form['tag_name']
    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Show details about a tag"""
    tag = Tag.query.get(tag_id)
    return render_template('/tag/details_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def show_edit_tag(tag_id):
    """Show the edit tag page"""
    tag = Tag.query.get(tag_id)
    return render_template('/tag/edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tag.name = request.form['new_tag_name']

    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')

