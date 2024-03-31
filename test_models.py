from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = True

with app.app_context():
    db.drop_all()
    db.create_all()

class UserModelTestCase(TestCase):
    """Tests model for Users."""

    def setUp(self):
        with app.app_context():
            User.query.delete()

    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_repr(self):
        new_user = User (
            first_name = "Bob",
            last_name = "Smith",
            image_url = 'https://marketplace.canva.com/EAFuJ5pCLLM/1/0/1600w/canva-black-and-gold-simple-business-man-linkedin-profile-picture-BM_NPo97JwE.jpg'
        )
        
        self.assertIn('Bob Smith', new_user.__repr__())
        self.assertIsInstance(new_user, User)