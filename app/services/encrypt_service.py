# ------------------------------- importaciones ------------------------------ #
from cryptography.fernet import Fernet
from app.models import Text
from app.repositories import TextRepository
import base64

# ----------------------------- fin importaciones ---------------------------- #

# ------------------------------- repositorios ------------------------------- #
text_repository = TextRepository()
# ----------------------------- fin repositorios ----------------------------- #


class EncryptService:
    """
    A class that provides encryption and decryption services for text content.
    """

    KEY_SIZE = 32
    
    def generate_fernet_key(self, key: str = None) -> bytes:
        """
        Generates a Fernet key.

        Args:
            key (str, optional): The key to use for generating the Fernet key. Defaults to None.

        Returns:
            bytes: The generated Fernet key.
        """
        if key is None:
            return Fernet.generate_key()
        return base64.urlsafe_b64encode(key.encode().ljust(self.KEY_SIZE, b"\0"))

    def encrypt_decrypt(self, text: Text, key: bytes, encrypt: bool) -> None:
        """
        Encrypts or decrypts the text content using the provided key.

        Args:
            text (Text): The text object to encrypt or decrypt.
            key (bytes): The key to use for encryption or decryption.
            encrypt (bool): True to encrypt, False to decrypt.

        Returns:
            None
        """
        fernet_key = Fernet(key)
        if encrypt:
            encrypted_content = fernet_key.encrypt(text.content.encode())
            text.content = encrypted_content.decode()
            text.encrypted = True
        else:
            decrypted_content = fernet_key.decrypt(text.content.encode())
            text.content = decrypted_content.decode()
            text.encrypted = False
        text_repository.save(text)

    def encrypt_content(self, text: Text, key: str = None) -> None:
        """
        Encrypts the content of the text object.

        Args:
            text (Text): The text object to encrypt.
            key (str, optional): The key to use for encryption. Defaults to None.

        Returns:
            None
        """
        key = self.generate_fernet_key(key)
        text.key = str(key.decode())
        self.encrypt_decrypt(text, key, encrypt=True)

    def decrypt_content(self, text: Text, decrypt_key: str) -> None:
        """
        Decrypts the content of the text object.

        Args:
            text (Text): The text object to decrypt.
            decrypt_key (str): The key to use for decryption.

        Returns:
            None
        """
        key = self.generate_fernet_key(decrypt_key)
        self.encrypt_decrypt(text, key, encrypt=False)
