import unittest
from flask import current_app
from app import create_app
from app.models import Role
from app import db
from app.services import RoleService

role_service = RoleService()

class RoleTestCase(unittest.TestCase):
    def setUp(self):
        # Crea una instancia de la aplicación Flask para pruebas
        self.app = create_app()
        # Crea un contexto de la aplicación y lo activa
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # Desactiva y limpia el contexto de la aplicación
        self.app_context.pop()

    # Prueba si la aplicación Flask se crea correctamente
    def test_app(self):
        self.assertIsNotNone(current_app)
    
    # Prueba la creación de roles
    def test_role(self):
        role=self.__get_role()
        self.assertTrue(role.name, self.ROL_NAME)
        self.assertTrue(role.description, self.ROL_DESCRIPCION)

    def test_role_save(self):
        role = self.__get_role()
        role_service.save(role)
        self.assertGreaterEqual(role.id, 1)
        self.assertTrue(role.name, self.ROL_NAME)
        self.assertTrue(role.description, self.ROL_DESCRIPCION)

    def test_role_update(self):
        role = self.__get_role()
        role_service.save(role)
        role.description = 'Administrator Updated'
        role_service.update(role, role.id)
        self.assertTrue(role.name, self.ROL_NAME)
        self.assertTrue(role.description, 'Administrator Updated')

    def test_role_delete(self):
        role = self.__get_role()
        role_service.save(role)
        role_service.delete(role)
        self.assertIsNone(role_service.find(role))

    def test_role_all(self):
        role = self.__get_role()
        role_service.save(role)
        roles = role_service.all()
        self.assertGreaterEqual(len(roles), 1)

    def test_role_find(self):
        role = self.__get_role()
        role_service.save(role)
        role_find = role_service.find(role.id)
        self.assertTrue(role_find.name, self.ROL_NAME)
        self.assertTrue(role_find.description, self.ROL_DESCRIPCION)

    def test_role_find_by_name(self):
        role = self.__get_role()
        role_service.save(role)
        role_find = role_service.find_by_name(self.ROL_NAME)
        self.assertTrue(role_find.name, self.ROL_NAME)
        self.assertTrue(role_find.description, self.ROL_DESCRIPCION)

    def __get_role(self) -> Role:
        role = Role()
        role.name = self.ROL_NAME
        role.description = self.ROL_DESCRIPCION
        return role

if __name__ == '__main__':
    # Ejecuta el conjunto de pruebas si el script se ejecuta directamente
    unittest.main()
