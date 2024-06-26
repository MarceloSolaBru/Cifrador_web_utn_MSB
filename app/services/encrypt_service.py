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

    KEY_SIZE = 32
    
    def generate_fernet_key(self, key: str = None) -> bytes:
        if key is None:
            return Fernet.generate_key()
        return base64.urlsafe_b64encode(key.encode().ljust(self.KEY_SIZE, b"\0"))

    def encrypt_decrypt(self, text: Text, key: bytes, encrypt: bool) -> None:
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
        key = self.generate_fernet_key(key)
        text.key = str(key.decode())
        self.encrypt_decrypt(text, key, encrypt=True)

    def decrypt_content(self, text: Text, decrypt_key: str) -> None:
        key = self.generate_fernet_key(decrypt_key)
        self.encrypt_decrypt(text, key, encrypt=False)
