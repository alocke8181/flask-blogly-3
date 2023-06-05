from unittest import TestCase
from flask import session
from app import app
from models import User

class AppTests(TestCase):
    """Integration tests for the app"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        """Test the home page response"""
        with self.client:
            resp = self.client.get('/')
            self.assertIn(b'<a href="/"><h1>Blogly!</h1></a>',resp.data)
            self.assertIn(b'<h2>Users</h2>',resp.data)
    
    def test_user_new_page(self):
        """Test the response of the new user form page"""
        with self.client:
            resp = self.client.get('/users/new')
            self.assertIn(b'<h2>Create a New User</h2>',resp.data)
            self.assertIn(b'<input type="text" name="first_name" placeholder="First Name">',resp.data)
            self.assertIn(b'<input type="text" name="last_name" placeholder="Last Name">',resp.data)
            self.assertIn(b'<input type="text" name="image_url" placeholder="URL">',resp.data)
            self.assertIn(b'<button type="submit">Submit</button>',resp.data)

    def test_user_info_page(self):
        """Test the response of the user info page"""
        with self.client:
            resp = self.client.get('users/1')
            self.assertIn(b'<img src',resp.data)
            self.assertIn(b'<button formaction="/users/1/edit" formmethod="GET">Edit</button>',resp.data)
            self.assertIn(b'<button formaction="/users/1/delete" formmethod="POST">Delete</button>',resp.data)

    def test_user_edit_page(self):
        """Test the user edit page"""
        with self.client:
            resp = self.client.get('users/1/edit')
            self.assertIn(b'<form method="POST">',resp.data)
            self.assertIn(b'<label for="new_first_name">First Name * </label>',resp.data)
            self.assertIn(b'<label for="new_last_name">Last Name * </label>',resp.data)
            self.assertIn(b'<label for="new_image_url">Profile Pic URL</label>',resp.data)