from flask import jsonify, Blueprint
from app.mapping.response_schema import ResponseSchema
from app.services.response_message import ResponseBuilder

home = Blueprint('home', __name__)
response_schema = ResponseSchema()

# Define una ruta para el endpoint '/' (raíz del sitio) dentro del blueprint 'home'
@home.route('/', methods=['GET'])
def index():
    response_builder = ResponseBuilder()
    response_builder.set_message("Bienvenidos").set_status_code(200).set_data(
        {"title": "API Auth"}
    )
    response = response_builder.build()
    return response_schema.dump(response), 200
