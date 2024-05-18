import unittest
from flask import current_app
from app import create_app, db
from app.models import User, UserData
from app.services import UserService

user_service = UserService()

class UserTestCase(unittest.TestCase):
    """
    Test User model
    Necesitamos aplicar principios como DRY (Don't Repeat Yourself) y KISS (Keep It Simple, Stupid).
    YAGNI (You Aren't Gonna Need It) y SOLID (Single Responsibility Principle).
    """

    def setUp(self):
        self.USERNAME_PRUEBA = 'pabloprats'
        self.EMAIL_PRUEBA = 'test@test.com'
        self.PASSWORD_PRUEBA = '123456'
        self.ADDRESS_PRUEBA = 'Address 1234'
        self.FIRSTNAME_PRUEBA = 'Pablo'
        self.LASTNAME_PRUEBA = 'Prats'
        self.PHONE_PRUEBA = '54260123456789'
        self.CITY_PRUEBA = 'San Rafael'
        self.COUNTRY_PRUEBA = 'Argentina'
        # Crea una instancia de la aplicación Flask para pruebas
        self.app = create_app()
        # Crea un contexto de la aplicación y lo activa
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Crea todas las tablas en la base de datos para las pruebas
        db.create_all()

    def tearDown(self):
        # Elimina la sesión de la base de datos y todas las tablas creadas
        db.session.remove()
        db.drop_all()
        # Desactiva y limpia el contexto de la aplicación
        self.app_context.pop()

    # Prueba si la aplicación Flask se crea correctamente
    def test_app(self):
        self.assertIsNotNone(current_app)

    # Prueba la creación de un usuario
    def test_user(self):
        user = self.__get_user()
        self.assertTrue(user.email, self.EMAIL_PRUEBA)
        self.assertTrue(user.username, self.USERNAME_PRUEBA)
        self.assertTrue(user.password, self.PASSWORD_PRUEBA)
        self.assertTrue(user.data.address, self.ADDRESS_PRUEBA)
        self.assertTrue(user.data.firstname, self.FIRSTNAME_PRUEBA)
        self.assertTrue(user.data.lastname, self.LASTNAME_PRUEBA)
        self.assertTrue(user.data.phone, self.PHONE_PRUEBA)     
    
    def test_user_save(self):

        user=self.__get_user()

        user_service.save(user)

        self.assertGreaterEqual(user.id, 1)
        self.assertTrue(user.email, self.EMAIL_PRUEBA)
        self.assertTrue(user.username, self.USERNAME_PRUEBA)
        self.assertIsNotNone(user.password)
        self.assertTrue(user_service.check_auth(user.username, self.PASSWORD_PRUEBA))
        self.assertTrue(user.data.address, self.ADDRESS_PRUEBA)
        self.assertTrue(user.data.firstname, self.FIRSTNAME_PRUEBA)
        self.assertTrue(user.data.lastname, self.LASTNAME_PRUEBA)
        self.assertTrue(user.data.phone, self.PHONE_PRUEBA)
        self.assertIsNotNone(user.data)

    def test_user_delete(self):

        user=self.__get_user()
        user_service.save(user)
        user_service.delete(user)
        self.assertIsNone(user_service.find(user))

    # * borrado en el codigo de user.py
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

    def __get_user(self):

        data = UserData()
        data.firstname = self.FIRSTNAME_PRUEBA
        data.lastname = self.LASTNAME_PRUEBA
        data.phone = self.PHONE_PRUEBA
        data.address = self.ADDRESS_PRUEBA
        data.city = self.CITY_PRUEBA
        data.country = self.COUNTRY_PRUEBA

        user = User(data)
        user.username = self.USERNAME_PRUEBA
        user.email = self.EMAIL_PRUEBA
        user.password = self.PASSWORD_PRUEBA
        
        return user

if __name__ == "__main__":
    # Ejecuta el conjunto de pruebas si el script se ejecuta directamente
    unittest.main()
