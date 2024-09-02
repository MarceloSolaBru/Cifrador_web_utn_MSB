from typing import List, Type
from app.models import User
from app import db
from app.models.user_data import UserData

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
        if entity is None:
            return None
        entity.username = user.username
        entity.email = user.email
        if user.password is not None:
            entity.password = user.password
        if user.data is not None:
            self.__update_data(entity, user.data)
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
        if user.data is not None:
            user.data.delete()
        user.delete()
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

    def find_by_email(self, email: str) -> User:
        """
        Finds a user by their email.

        Parameters:
            email (str): The email of the user to find.

        Returns:
            User: The user object if found, None otherwise.
        """
        return db.session.query(User).filter(User.email == email).one_or_none()

    def __update_data(self, entity: User, data: UserData):
        """
        Update the data of a user entity with the provided data.

        Args:
            entity (User): The user entity to update.
            data (UserData): The new data to update the user entity with.

        Returns:
            None
        """
        entity.data.firstname = data.firstname
        entity.data.lastname = data.lastname
        entity.data.phone = data.phone
        entity.data.address = data.address
        entity.data.city = data.city
        entity.data.country = data.country