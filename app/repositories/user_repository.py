from typing import List, Type
from app.models import User
from app import db


class UserRepository:
    """
    Aplicamos Responsabilidad Única y el Patrón Repository https://martinfowler.com/eaaCatalog/repository.html
    """

    def save(self, user: User) -> User:
        """
        Saves a user object to the database.

        Args:
            user (User): The user object to be saved.

        Returns:
            User: The saved user object.
        """
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user: User, id: int) -> User:
        """
        Updates a user object in the database.

        Args:
            user (User): The updated user object.
            id (int): The ID of the user to be updated.

        Returns:
            User: The updated user object.
        """
        entity = self.find(id)
        entity.username = user.username
        entity.email = user.email
        db.session.add(entity)
        db.session.commit()
        return entity

    def delete(self, user: User) -> None:
        """
        Deletes a user object from the database.

        Args:
            user (User): The user object to be deleted.

        Returns:
            None
        """
        db.session.delete(user)
        db.session.commit()

    def all(self) -> List[User]:
        """
        Retrieves all user objects from the database.

        Returns:
            List[User]: A list of all user objects.
        """
        users = db.session.query(User).all()
        return users

    def find(self, id: int) -> User:
        """
        Retrieves a user object from the database by ID.

        Args:
            id (int): The ID of the user to be retrieved.

        Returns:
            User: The retrieved user object, or None if not found.
        """
        if id is None or id == 0:
            return None
        try:
            return db.session.query(User).filter(User.id == id).one()
        except:
            return None

    def find_by_username(self, username: str):
        """
        Retrieves a user object from the database by username.

        Args:
            username (str): The username of the user to be retrieved.

        Returns:
            User: The retrieved user object, or None if not found.
        """
        return db.session.query(User).filter(User.username == username).one_or_none()

    def find_by_email(self, email: str) -> List[User]:
        """
        Retrieves a list of user objects from the database by email.

        Args:
            email (str): The email to search for.

        Returns:
            List[User]: A list of user objects matching the email.
        """
        return db.session.query(User).filter(User.email.like(f"%{email}%")).all()
