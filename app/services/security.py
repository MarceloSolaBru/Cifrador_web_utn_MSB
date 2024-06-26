from abc import ABC, abstractmethod
from passlib.hash import pbkdf2_sha256
from werkzeug.security import generate_password_hash, check_password_hash


class AbstractSecurity(ABC):
    @abstractmethod
    def generate_password(self, password: str) -> str:
        """
        Abstract method to generate a password hash.

        Args:
            password (str): The plain password.

        Returns:
            str: The hashed password.
        """
        pass

    @abstractmethod
    def check_password(self, hashed_password: str, plain_password: str) -> bool:
        """
        Abstract method to check if a plain password matches a hashed password.

        Args:
            hashed_password (str): The hashed password.
            plain_password (str): The plain password.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        pass


class WerkzeugSecurity(AbstractSecurity):
    def generate_password(self, password: str) -> str:
        """
        Generates a password hash using Werkzeug's generate_password_hash function.

        Args:
            password (str): The plain password.

        Returns:
            str: The hashed password.
        """
        return generate_password_hash(password)

    def check_password(self, hashed_password: str, plain_password: str) -> bool:
        """
        Checks if a plain password matches a hashed password using Werkzeug's check_password_hash function.

        Args:
            hashed_password (str): The hashed password.
            plain_password (str): The plain password.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return check_password_hash(hashed_password, plain_password)


class PassLibSecurity(AbstractSecurity):
    def generate_password(self, password: str) -> str:
        """
        Generates a password hash using PassLib's pbkdf2_sha256.hash function.

        Args:
            password (str): The plain password.

        Returns:
            str: The hashed password.
        """
        return pbkdf2_sha256.hash(password)

    def check_password(self, hashed_password: str, plain_password: str) -> bool:
        """
        Checks if a plain password matches a hashed password using PassLib's pbkdf2_sha256.verify function.

        Args:
            hashed_password (str): The hashed password.
            plain_password (str): The plain password.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return pbkdf2_sha256.verify(plain_password, hashed_password)


class SecurityManager:
    def __init__(self, security: AbstractSecurity):
        """
        Initializes a SecurityManager instance.

        Args:
            security (AbstractSecurity): An instance of a class implementing the AbstractSecurity interface.
        """
        self.__security = security

    def generate_password(self, password: str) -> str:
        """
        Generates a password hash using the provided security implementation.

        Args:
            password (str): The plain password.

        Returns:
            str: The hashed password.
        """
        return self.__security.generate_password(password)

    def check_password(self, hashed_password: str, plain_password: str) -> bool:
        """
        Checks if a plain password matches a hashed password using the provided security implementation.

        Args:
            hashed_password (str): The hashed password.
            plain_password (str): The plain password.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return self.__security.check_password(hashed_password, plain_password)
