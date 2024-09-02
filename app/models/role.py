# Importa el decorador dataclass desde el módulo dataclasses
from dataclasses import dataclass
from .user import User

from app import db

from app.models.relations import users_roles
from app import db


# Define una clase llamada Role utilizando el decorador dataclass
@dataclass(init=False, repr=True, eq=True)
class Role(db.Model):
    """
    Role model represents a role in the application.
    Attributes:
        id (int): The unique identifier of the role.
        name (str): The name of the role.
        description (str): The description of the role.
    Relationships:
        users (list): A list of users associated with the role.
    Methods:
        save(): Saves the role to the database.
        add_user(user): Adds a user to the role.
        remove_user(user): Removes a user from the role.
    """
    __tablename__ = "roles"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(80), unique=True, nullable=False)
    description: str = db.Column(db.String(255), nullable=False)
    # Relacion Muchos a Muchos bidireccional con User
    users = db.relationship("User", secondary=users_roles, back_populates="roles")

    def save(self):
        """
        Saves the current instance of the Role model to the database.

        Returns:
            self: The saved instance of the Role model.
        """
        db.session.add(self)
        db.session.commit()
        return self

    def add_user(self, user):
        """
        Adds a user to the role.

        Parameters:
        - user: The user to be added.

        Returns:
        None
        """
        if user not in self.users:
            self.users.append(user)

    def remove_user(self, user):
        """
        Removes a user from the role.

        Parameters:
        - user: The user to be removed from the role.

        Returns:
        None
        """
        if user in self.users:
            self.users.remove(user)
