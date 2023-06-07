from unittest import TestCase
from flask import session
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    db.drop_all()
    db.create_all()

class AppTests(TestCase):
    """Test for the app"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        with app.app_context():
            Post.query.delete()
            User.query.delete()
            

    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_home(self):
        """Test the home page response"""
        with self.client, app.app_context():
            resp = self.client.get('/')
            self.assertIn(b'<a href="/"><h1>Blogly!</h1></a>',resp.data)
            self.assertIn(b'<h2>Users</h2>',resp.data)
    
    def test_user_new_page(self):
        """Test the response of the new user form page"""
        with self.client, app.app_context():
            resp = self.client.get('/users/new')
            self.assertIn(b'<h2>Create a New User</h2>',resp.data)
            self.assertIn(b'<input type="text" name="first_name" placeholder="First Name">',resp.data)
            self.assertIn(b'<input type="text" name="last_name" placeholder="Last Name">',resp.data)
            self.assertIn(b'<input type="text" name="image_url" placeholder="URL">',resp.data)
            self.assertIn(b'<button type="submit">Submit</button>',resp.data)

    def test_create_new_user(self):
        """Testing the create user functionality"""
        with self.client, app.app_context():
            resp = self.client.post('/users/new', follow_redirects=True, content_type='multipart/form-data',
            data = {
                'first_name':'Test',
                'last_name':'McTest',
                'image_url':'https://i.imgur.com/GuAB8OE.jpeg'
            })
            self.assertIn(b'<a href="/users/1">Test McTest</a>', resp.data)
            self.assertEquals(User.query.get(1).first_name, 'Test')
            self.assertEquals(User.query.get(1).last_name, 'McTest')
            self.assertEquals(User.query.get(1).image_url, 'https://i.imgur.com/GuAB8OE.jpeg')

    def test_show_user(self):
        """Test the response of the user info page"""
        with self.client, app.app_context():
            self.client.post('/users/new', follow_redirects=True, content_type='multipart/form-data',
            data = {
                'first_name':'Test',
                'last_name':'McTest',
                'image_url':'https://i.imgur.com/GuAB8OE.jpeg'
            })
            resp = self.client.get('/users/1')
            self.assertIn(b'<img src="https://i.imgur.com/GuAB8OE.jpeg" width="200" height="200">',resp.data)
            self.assertIn(b'<h2>Test McTest</h2>',resp.data)

    def test_edit_user(self):
        """Test the user edit page"""
        with self.client, app.app_context():
            self.client.post('/users/new', follow_redirects=True, content_type='multipart/form-data',
            data = {
                'first_name':'Test',
                'last_name':'McTest',
                'image_url':'https://i.imgur.com/GuAB8OE.jpeg'
            })
            resp = self.client.post('/users/1/edit', follow_redirects=True, content_type='multipart/form-data',
            data = {
                'new_first_name':'Tester',
                'new_last_name':'Testing',
                'new_image_url':'https://i.imgur.com/GuAB8OE.jpeg'
            })
            self.assertIn(b'<img src="https://i.imgur.com/GuAB8OE.jpeg" width="200" height="200">',resp.data)
            self.assertIn(b'<h2>Tester Testing</h2>',resp.data)
    
    def test_delete_user(self):
        """Testing the delete user functionality"""
        with self.client, app.app_context():
            self.client.post('/users/new', follow_redirects=True, content_type='multipart/form-data',
            data = {
                'first_name':'Test',
                'last_name':'McTest',
                'image_url':'https://i.imgur.com/GuAB8OE.jpeg'
            })
            resp_delete = self.client.post('users/1/delete', follow_redirects=True)
            self.assertIn(b'<h2>Users</h2>', resp_delete.data)
            self.assertRaises(Exception, User.query.get(1))

    def test_create_post(self):
        """Testing the create post functionality"""
        with self.client, app.app_context():
            self.client.post('/users/new', follow_redirects=True, content_type='multipart/form-data',
            data = {
                'first_name':'Test',
                'last_name':'McTest',
                'image_url':'https://i.imgur.com/GuAB8OE.jpeg'
            })
            resp = self.client.post('/users/1/posts/new', follow_redirects=True, content_type='multipart/form-data',
            data = {
                'title':'Test Post',
                'content':'Please ignore',
            })
            
            self.assertIn(b'<h2>Test Post</h2>', resp.data)
            self.assertIn(b'Please ignore', resp.data)

    def test_edit_post(self):
        with self.client, app.app_context():
            self.client.post('/users/new', follow_redirects=True, content_type='multipart/form-data',
            data = {
                'first_name':'Test',
                'last_name':'McTest',
                'image_url':'https://i.imgur.com/GuAB8OE.jpeg'
            })
            self.client.post('/users/1/posts/new', follow_redirects=True, content_type='multipart/form-data',
            data = {
                'title':'Test Post',
                'content':'Please ignore',
            })
            resp = self.client.post('/posts/1/edit', follow_redirects=True, content_type='multipart/form-data',
            data = {
                'title':'New Test Post',
                'content':'Please continue to ignore',
            })
            self.assertIn(b'<h2>New Test Post</h2>', resp.data)
            self.assertIn(b'Please continue to ignore', resp.data)

    def test_delete_post(self):
        with self.client, app.app_context():
            self.client.post('/users/new', follow_redirects=True, content_type='multipart/form-data',
            data = {
                'first_name':'Test',
                'last_name':'McTest',
                'image_url':'https://i.imgur.com/GuAB8OE.jpeg'
            })
            self.client.post('/users/1/posts/new', follow_redirects=True, content_type='multipart/form-data',
            data = {
                'title':'Test Post',
                'content':'Please ignore',
            })
            resp = self.client.get('/posts/1/delete', follow_redirects=True)
            self.assertIn(b'<img src="https://i.imgur.com/GuAB8OE.jpeg" width="200" height="200">',resp.data)
            self.assertIn(b'<h2>Test McTest</h2>',resp.data)
            self.assertRaises(Exception, Post.query.get(1))



