from typing import List
from app.models import User
from app.repositories import UserRepository
from app.services import SecurityManager, WerkzeugSecurity

repository = UserRepository()


class UserService:
    def __init__(self) -> None:
        self.__security = SecurityManager(WerkzeugSecurity())

    def save(self, user: User) -> User:
        """
        Save a user in the repository.

        Args:
            user (User): The user object to be saved.

        Returns:
            User: The saved user object.
        """
        # TODO: Implementar auditoria
        user.password = self.__security.generate_password(user.password)
        return repository.save(user)

    def update(self, user: User, id: int) -> User:
        """
        Update a user in the repository.

        Args:
            user (User): The updated user object.
            id (int): The ID of the user to be updated.

        Returns:
            User: The updated user object.
        """
        # TODO: Implementar auditoria
        return repository.update(user, id)

    def delete(self, user: User) -> None:
        """
        Delete a user from the repository.

        Args:
            user (User): The user object to be deleted.
        """
        # TODO: Implementar auditoria
        repository.delete(user)

    def all(self) -> List[User]:
        """
        Get all users from the repository.

        Returns:
            List[User]: A list of all users.
        """
        return repository.all()

    def find(self, id: int) -> User:
        """
        Find a user by ID in the repository.

        Args:
            id (int): The ID of the user to find.

        Returns:
            User: The found user object.
        """
        return repository.find(id)

    def find_by_username(self, username: str):
        """
        Find a user by username in the repository.

        Args:
            username (str): The username of the user to find.

        Returns:
            User: The found user object.
        """
        return repository.find_by_username(username)

    def find_by_email(self, email) -> User:
        """
        Find a user by email in the repository.

        Args:
            email: The email of the user to find.

        Returns:
            User: The found user object.
        """
        return repository.find_by_email(email)

    def check_auth(self, username, password) -> bool:
        """
        Check if the provided username and password are valid.

        Args:
            username (str): The username to check.
            password (str): The password to check.

        Returns:
            bool: True if the username and password are valid, False otherwise.
        """
        user = self.find_by_username(username)
        if user is not None:
            return self.__security.check_password(user.password, password)
        else:
            return False
