# ------------------------------- importaciones ------------------------------ #
import unittest
from flask import current_app
from app import create_app, db
from app.models import Text
from app.services import UserService, EncryptService, TextService
from app.repositories import TextRepository
from app.models.user import User
from app.models.user_data import UserData
# ----------------------------- fin importaciones ---------------------------- #

# ------------------------- servicios y repositorios ------------------------- #
encrypt_service = EncryptService()
text_repository = TextRepository()
# ----------------------- fin servicios y repositorios ----------------------- #


class TextTestCase(unittest.TestCase):
    # * METODO PARA CREAR LA BASE DE DATOS
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.content = "Hola mundo"
        self.length = len(self.content)
        self.language = "es"

    # * METODO PARA DESTRUIR LA BASE DE DATOS
    def tearDown(self):
        db.session.remove()

    # * GETTER DE TEXTO
    def __get_text(self):
        text = Text()
        text.content = self.content
        text.length = self.length
        text.language = self.language
        return text

    # * METODO PARA COMPROBAR QUE LOS ATRIBUTOS DE TEXTO SEAN CORRECTOS
    def assert_text_content(self, text):
        self.assertEqual(text.content, self.content)
        self.assertEqual(text.length, self.length)
        self.assertEqual(text.language, self.language)

    def test_text(self):
        text = self.__get_text()
        self.assert_text_content(text)

    def test_text_save(self):
        text = self.__get_text()
        text_repository.save(text)
        self.assertGreaterEqual(text.id, 1)
        self.assert_text_content(text)

    def test_text_delete(self):
        text = self.__get_text()
        text_repository.save(text)
        text_repository.delete(text)
        self.assertIsNone(Text.query.get(text.id))

    def test_text_find(self):
        text = self.__get_text()
        text_repository.save(text)
        text_find = text_repository.find(text.id) 
        self.assertIsNotNone(text_find)
        self.assertEqual(text_find.id, text.id)
        self.assert_text_content(text_find)

    def test_auto_encrypt_content(self):
        text = self.__get_text()
        text_repository.save(text)
        encrypt_service.encrypt_content(text)
        self.assertNotEqual(text.content, self.content)
        self.assertTrue(text.encrypted)

    def test_manual_encrypt_content(self):
        text = self.__get_text()
        text_repository.save(text)
        key = "secret_key"
        encrypt_service.encrypt_content(text, key)
        self.assertNotEqual(text.content, self.content)
        self.assertTrue(text.encrypted)

    def test_decrypt_content(self):
        text = self.__get_text()
        text_repository.save(text)
        key = "secret_key"
        encrypt_service.encrypt_content(text, key)
        encrypt_service.decrypt_content(text, key)
        self.assertEqual(text.content, self.content)

    def test_edit_content(self):
        text = self.__get_text()
        text_repository.save(text)
        text_service = TextService()
        new_content = "Hello world"
        text_service.edit_content(text, new_content)
        self.assertEqual(text.content, new_content)
        new_content = "Hello world2"
        text_service.edit_content(text, new_content)
        self.assertEqual(text.content, new_content)
        new_content = "Hello world3"
        text_service.edit_content(text, new_content)
        self.assertEqual(text.content, new_content)

    # test para comprobar que funciona la relacion entres usuarios y textos
    def test_user_text(self):
        from app.models.user import User
        from app.models.user_data import UserData

        # Crea un objeto UserData con información de prueba
        data = UserData(
            firstname="Pablo",
            lastname="Prats",
            address="Address 1234",
            city="San Rafael",
            country="Argentina",
            phone="54260123456789",
        )

        # Crea un objeto User y establece sus atributos
        user = User(data)
        user.email = "test@test.com"
        user.username = "pabloprats"
        user.password = "Qvv3r7y"
        user_service = UserService()
        user_service.save(user)

        # Crea un objeto Text y establece sus atributos
        text = self.__get_text()
        text.user_id = user.id
        text_repository.save(text)

    def test_text_json(self):
        text = self.__get_text()
        text_repository.save(text)
        text_json = text.to_json()
        self.assertEqual(text_json["id"], text.id)
        self.assertEqual(text_json["content"], text.content)
        self.assertEqual(text_json["length"], text.length)
        self.assertEqual(text_json["language"], text.language)
        self.assertEqual(text_json["encrypted"], text.encrypted)
        self.assertEqual(text_json["key"], text.key)


if __name__ == "__main__":
    unittest.main()
