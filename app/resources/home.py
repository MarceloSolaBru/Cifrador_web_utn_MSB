from flask import jsonify, Blueprint

home = Blueprint('home', __name__)

# Define una ruta para el endpoint '/' (raíz del sitio) dentro del blueprint 'home'
@home.route('/', methods=['GET'])
def index():
    resp = jsonify("OK")
    resp.status_code = 200
    return resp
