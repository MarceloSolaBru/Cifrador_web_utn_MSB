import unittest
from flask import current_app
from app import create_app
from app.mapping.response_schema import ResponseSchema
from app.services.response_message import ResponseBuilder
import os

class AppTestCase(unittest.TestCase):
    # Método de configuración que se ejecuta antes de cada prueba
    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        # Crea una instancia de la aplicación Flask para pruebas
        self.app = create_app()
        # Crea un contexto de la aplicación y lo activa
        self.app_context = self.app.app_context()
        self.app_context.push()

    # Método de limpieza que se ejecuta después de cada prueba
    def tearDown(self):
        # Desactiva y limpia el contexto de la aplicación
        self.app_context.pop()

    # Método de prueba para verificar si la aplicación Flask se crea correctamente
    def test_app(self):
        # Verifica que el objeto current_app no sea None
        self.assertIsNotNone(current_app)

    def test_index(self):
        message = ResponseBuilder().add_message("Bienvenidos").add_status_code(200).add_data({'title': 'API Auth'}).build()
        client = self.app.test_client(use_cookies=True)
        responseSchema = ResponseSchema()
        #TODO: La URL de la API debe cambiarse por una variable de entorno
        response = client.get('http://localhost:5000/api/v1/')
        self.assertEqual(response.status_code, 200)
        response = responseSchema.load(response.get_json())
        self.assertEqual(message.message, response['message'])
        self.assertEqual(message.status_code, response['status_code'])
        self.assertEqual(message.data, response['data'])
        

# Ejecuta el conjunto de pruebas si el script se ejecuta directamente
if __name__ == '__main__':
    unittest.main()
