import unittest
from flask import current_app
from app import create_app, db
from app.models import User, UserData

class AppTestCase(unittest.TestCase):
    def setUp(self):
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
        # Crea un objeto UserData con información de prueba
        data = UserData()
        data.surname = 'surname'
        data.address = 'address 1234'
        data.city = 'city'
        data.country = 'country'
        data.phone = '542605502105'
        
        # Crea un objeto User y establece sus atributos
        user = User(data)
        user.email = 'test@test.com'
        user.username = 'test'
        user.password = 'test1234'

        # Verifica que los atributos del usuario se hayan establecido correctamente
        self.assertTrue(user.email, 'test@test.com')
        self.assertTrue(user.username, 'test')
        self.assertTrue(user.password, 'test1234')
        self.assertIsNotNone(user.data)
        self.assertTrue(user.data.surname, 'surname')
        self.assertTrue(user.data.address, 'address 1234')
        self.assertTrue(user.data.phone, '542605502105')   

if __name__ == '__main__':
    # Ejecuta el conjunto de pruebas si el script se ejecuta directamente
    unittest.main()
