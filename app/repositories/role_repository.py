from typing import List
from app.models import Role
from app import db


class RoleRepository:
    """
    Repository class for managing Role objects in the database.
    """

    def save(self, role: Role) -> Role:
        """
        Save a Role object to the database.

        Args:
            role (Role): The Role object to be saved.

        Returns:
            Role: The saved Role object.
        """
        db.session.add(role)
        db.session.commit()
        return role

    def update(self, role: Role, id: int) -> Role:
        """
        Update a Role object in the database.

        Args:
            role (Role): The updated Role object.
            id (int): The ID of the Role object to be updated.

        Returns:
            Role: The updated Role object.
        """
        entity = self.find(id)
        entity.name = role.name
        entity.description = role.description
        db.session.add(entity)
        db.session.commit()
        return role

    def delete(self, role: Role) -> None:
        """
        Delete a Role object from the database.

        Args:
            role (Role): The Role object to be deleted.

        Returns:
            None
        """
        db.session.delete(role)
        db.session.commit()

    def all(self) -> List[Role]:
        """
        Retrieve all Role objects from the database.

        Returns:
            List[Role]: A list of all Role objects.
        """
        return db.session.query(Role).all()

    def find(self, id: int) -> Role:
        """
        Find a Role object by its ID.

        Args:
            id (int): The ID of the Role object to be found.

        Returns:
            Role: The found Role object, or None if not found.
        """
        if id is None or id == 0:
            return None
        try:
            return db.session.query(Role).filter(Role.id == id).one()
        except:
            return None

    def find_by_name(self, name: str) -> Role:
        """
        Find a Role object by its name.

        Args:
            name (str): The name of the Role object to be found.

        Returns:
            Role: The found Role object, or None if not found.
        """
        return db.session.query(Role).filter(Role.name == name).one_or_none()
