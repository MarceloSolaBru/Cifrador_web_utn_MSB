import unittest
from flask import current_app
from app import create_app, db
from app.models.text_history import TextHistory
from app.models.text import Text
from app.models.user import User  # Make sure to import the User model

class TextHistoryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Add a user to avoid ForeignKey constraint violations
        user = User(username="testuser", email="test@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()

        # Store the user_id for use in tests
        self.user_id = user.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def initialize_text(self, text):
        text.content = "Hola mundo1"
        text.length = len(text.content)
        text.language = "es"
        text.user_id = self.user_id  # Use the user_id stored in setUp

    def test_text_history_save(self):
        text = Text()
        self.initialize_text(text)
        db.session.add(text)
        db.session.commit()  # Save the text to the database

        # Save a version of the text
        history = TextHistory()
        history.text_id = text.id
        history.content = "Hola mundo"
        db.session.add(history)
        db.session.commit()

        self.assertGreaterEqual(history.id, 1)
        self.assertEqual(history.text_id, text.id)
        self.assertEqual(history.content, "Hola mundo")

    def test_change_to_version(self):
        # Create a text and save two versions
        text = Text()
        self.initialize_text(text)
        db.session.add(text)
        db.session.commit()  # Save the text to the database

        version1 = TextHistory()
        version1.text_id = text.id
        version1.content = "Hola mundo"
        db.session.add(version1)
        db.session.commit()

        version2 = TextHistory()
        version2.text_id = text.id
        version2.content = "Bonjour monde"
        db.session.add(version2)
        db.session.commit()

        # Change to the first version and verify the content change
        version1.change_to_version(version1.id)
        updated_text = Text.query.get(text.id)
        self.assertEqual(updated_text.content, version1.content)

        # Change to the second version and verify the content change
        version2.change_to_version(version2.id)
        updated_text = Text.query.get(text.id)
        self.assertEqual(updated_text.content, version2.content)

if __name__ == "__main__":
    unittest.main()
