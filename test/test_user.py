import unittest
from flask import current_app
from app.models import User, UserData
from app import create_app, db
from app.services import UserService

user_service = UserService()


class UserTestCase(unittest.TestCase):
    """
    Test User model
    Necesitamos aplicar principios como DRY (Don't Repeat Yourself) y KISS (Keep It Simple, Stupid).
    YAGNI (You Aren't Gonna Need It) y SOLID (Single Responsibility Principle).
    """

    def setUp(self):
        self.USERNAME_PRUEBA = "pabloprats"
        self.EMAIL_PRUEBA = "test@test.com"
        self.PASSWORD_PRUEBA = "123456"
        self.ADDRESS_PRUEBA = "Address 1234"
        self.FIRSTNAME_PRUEBA = "Pablo"
        self.LASTNAME_PRUEBA = "Prats"
        self.PHONE_PRUEBA = "54260123456789"
        self.CITY_PRUEBA = "San Rafael"
        self.COUNTRY_PRUEBA = "Argentina"

        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def __get_user(self):
        username = self.USERNAME_PRUEBA
        email = self.EMAIL_PRUEBA
        password = self.PASSWORD_PRUEBA
        user=User (username, password, email)
        return user

    def test_user(self):

        user = self.__get_user()

        self.assertTrue(user.email, self.EMAIL_PRUEBA)
        self.assertTrue(user.username, self.USERNAME_PRUEBA)
        self.assertTrue(user.password, self.PASSWORD_PRUEBA)

    def test_user_save(self):

        user = self.__get_user()

        user_service.save(user)

        self.assertGreaterEqual(user.id, 1)
        self.assertTrue(user.email, self.EMAIL_PRUEBA)
        self.assertTrue(user.username, self.USERNAME_PRUEBA)
        self.assertIsNotNone(user.password)
        self.assertTrue(user_service.check_auth(user.username, self.PASSWORD_PRUEBA))
        self.assertIsNotNone(user.data)
        self.assertTrue(user.data.address, self.ADDRESS_PRUEBA)
        self.assertTrue(user.data.firstname, self.FIRSTNAME_PRUEBA)
        self.assertTrue(user.data.lastname, self.LASTNAME_PRUEBA)
        self.assertTrue(user.data.phone, self.PHONE_PRUEBA)

    def test_user_delete(self):

        user = self.__get_user()

        user_service.save(user)

        # borro el usuario
        user_service.delete(user)
        self.assertIsNone(user_service.find(user))

    def test_user_all(self):

        user = self.__get_user()
        user_service.save(user)

        users = user_service.all()
        self.assertGreaterEqual(len(users), 1)

    def test_user_find(self):

        user = self.__get_user()
        user_service.save(user)

        user_find = user_service.find(1)
        self.assertIsNotNone(user_find)
        self.assertEqual(user_find.id, user.id)
        self.assertEqual(user_find.email, user.email)



if __name__ == "__main__":
    unittest.main()
