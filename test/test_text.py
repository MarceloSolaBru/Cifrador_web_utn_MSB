import unittest
from flask import current_app
from app import create_app, db
from app.models import Text, TextHistory
from cryptography.fernet import Fernet
from app.services import UserService
from app.models.user import User


class TextTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Add a user to avoid ForeignKey constraint violations
        self.user = User(email="test@test.com", username="pabloprats", password="Qvv3r7y")
        UserService().save(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def set_text_attributes(self, text):
        text.content = "Hola mundo"
        text.length = len(text.content)
        text.language = "es"
        text.user_id = self.user.id

    def assert_text_content(self, text):
        self.assertEqual(text.content, "Hola mundo")
        self.assertEqual(text.length, 10)
        self.assertEqual(text.language, "es")

    def test_text(self):
        text = Text()
        self.set_text_attributes(text)
        self.assert_text_content(text)

    def test_text_save(self):
        text = Text()
        self.set_text_attributes(text)
        text.save()
        self.assertGreaterEqual(text.id, 1)
        self.assert_text_content(text)

    def test_text_delete(self):
        text = Text()
        self.set_text_attributes(text)
        text.save()
        text.delete()
        self.assertIsNone(Text.query.get(text.id))

    def test_text_find(self):
        text = Text()
        self.set_text_attributes(text)
        text.save()
        text_find = Text.find(text.id)
        self.assertIsNotNone(text_find)
        self.assertEqual(text_find.id, text.id)
        self.assertEqual(text_find.content, text.content)

    def test_encrypt_content(self):
        text = Text()
        self.set_text_attributes(text)
        text.save()

        key = Fernet.generate_key()

        text.encrypt_content(key)

        self.assertNotEqual(text.content, "Hola mundo")
        self.assertIsInstance(text.content, str)

    def test_decrypt_content(self):
        text = Text()
        self.set_text_attributes(text)
        text.save()

        key = Fernet.generate_key()
        text.encrypt_content(key)

        text.decrypt_content(key)

        self.assertEqual(text.content, "Hola mundo")

    def test_change_content(self):
        # Create a Text object and save a version
        text = Text()
        self.set_text_attributes(text)
        text.save()

        old_content = text.content

        # Change the content
        new_content = "Hola mundo"
        text.change_content(new_content)

        # Verify that the content has changed
        self.assertEqual(text.content, new_content)

        # Verify that the previous version is saved in TextHistory
        history = TextHistory.query.filter_by(text_id=text.id).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.content, old_content)

    def test_user_text(self):
        # Create a Text object and associate it with a user
        text = Text()
        self.set_text_attributes(text)
        text.save()

        self.assertEqual(text.user_id, self.user.id)


if __name__ == "__main__":
    unittest.main()
