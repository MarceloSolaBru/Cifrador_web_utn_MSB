from dataclasses import dataclass
from .user_data import UserData
from app import db
from typing import List
from app.models.relations import users_roles
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@dataclass(init=False, repr=True, eq=True)
class User(db.Model, UserMixin):  # Hereda de db.Model, lo que indica que es un modelo de base de datos
    __tablename__ = "users"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    password: str = db.Column('password', db.String(255), nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    users_rs = db.relationship("Text", backref="user", lazy=True)
    data = db.relationship("UserData", uselist=False, back_populates="user")  # type: ignore
    roles = db.relationship("Role", secondary=users_roles, back_populates='users')
    role_id: int = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def add_role(self, role):
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role):
        if role in self.roles:
            self.roles.remove(role)
    
    def is_active(self):
        # aca va la lógica para determinar si el usuario está activo
        return True  # devuelve True si el usuario siempre está activo
