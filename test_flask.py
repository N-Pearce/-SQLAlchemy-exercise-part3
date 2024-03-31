from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = True

with app.app_context():
    db.drop_all()
    db.create_all()

class UsersViewTestCase(TestCase):
    """Tests that the flask app with Users works"""

    def setUp(self):
        """Add sample user"""

        with app.app_context():
            User.query.delete()

        user = User(first_name="Terrence", last_name="Hill")
        
        with app.app_context():
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Terrence Hill', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertIn('Terrence Hill', html)
            self.assertIn('Edit', html)
            self.assertIn('Delete', html)
    
    
    def test_show_edit_form(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertIn('First Name: ', html)
            self.assertIn('Last Name: ', html)
            self.assertIn('Image URL: ', html)
            self.assertIn('Confirm', html)
            self.assertIn('Cancel', html)
            
    def test_show_add_user_form(self):
        with app.test_client() as client:
            resp = client.get(f'/add-user')
            html = resp.get_data(as_text=True)

            self.assertIn('First Name: ', html)
            self.assertIn('Last Name: ', html)
            self.assertIn('Image URL: ', html)
            self.assertIn('Add', html)
    
    