# Importa el decorador dataclass desde el módulo dataclasses
from dataclasses import dataclass
# Importa la clase UserData desde el archivo user_data.py en el mismo directorio
from .user_data import UserData
# Importa la instancia db desde el módulo app, que parece ser un objeto de SQLAlchemy
from app import db

# Define una clase llamada User utilizando el decorador dataclass
@dataclass(init=False, repr=True, eq=True)
class User(db.Model):  # Hereda de db.Model, lo que indica que es un modelo de base de datos
    __tablename__ = 'users'  # Nombre de la tabla en la base de datos
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Columna de clave primaria
    username: str = db.Column(db.String(80), unique=True, nullable=False)  # Columna para el nombre de usuario
    password: str = db.Column(db.String(120), nullable=False)  # Columna para la contraseña del usuario
    email: str = db.Column(db.String(120), unique=True, nullable=False)  # Columna para el correo electrónico del usuario
    
    # Relación con la tabla 'UserData' (datos de usuario), establecida a través de la propiedad 'user' en la clase UserData
    data = db.relationship('UserData', uselist=False, back_populates='user') # type: ignore

    # Constructor de la clase User, que puede recibir un objeto UserData opcionalmente
    def __init__(self, user_data: UserData = None):
        # Si se proporciona un objeto UserData, se asigna a la propiedad 'data' del usuario
        if user_data:
            self.data = user_data
        else:
            # Si no se proporciona ningún objeto UserData, se crea uno nuevo y se asigna al usuario
            self.data = UserData()
