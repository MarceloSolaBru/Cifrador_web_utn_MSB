from dataclasses import dataclass
from app import db

# Define una clase llamada UserData utilizando el decorador dataclass
@dataclass(init=False, repr=True, eq=True)
class UserData(db.Model):  # Hereda de db.Model, lo que indica que es un modelo de base de datos
    __tablename__ = "users_data"  # Nombre de la tabla en la base de datos
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Columna de clave primaria
    firstname: str = db.Column(db.String(80), nullable=False)
    lastname: str = db.Column(db.String(80), nullable=False)
    phone: str = db.Column(db.String(120), nullable=False)  
    address: str = db.Column(db.String(120), nullable=False)  
    city: str = db.Column(db.String(120), nullable=False)  
    country: str = db.Column(db.String(120), nullable=False) 

    # Columna de clave externa para establecer la relación con la tabla 'users' (usuarios)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))

    # Relación con la tabla 'User' (usuarios), establecida a través de la columna 'user_id'
    user = db.relationship("User", back_populates="data", uselist=False)
    
    #Relacion Muchos a Uno bidireccional con Profile
    profile_id = db.Column('profile_id', db.Integer, db.ForeignKey('profiles.id'))
    profile = db.relationship("Profile", back_populates='data')