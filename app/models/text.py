# ------------------------------- importaciones ------------------------------ #
from dataclasses import dataclass
from app import db

# ----------------------------- fin importaciones ---------------------------- #


@dataclass(init=False, repr=True, eq=True)
class Text(db.Model):
    class Text:
        """
        Represents a text object.
        Attributes:
            id (int): The unique identifier of the text.
            content (str): The content of the text.
            length (int): The length of the text.
            language (str): The language of the text.
            encrypted (bool): Indicates if the text is encrypted or not.
            key (str): The encryption key for the text.
            user_id (int): The foreign key referencing the user who owns the text.
            histories (list): A list of text history objects associated with the text.
        Methods:
            __init__(self, content: str = "default text", language: str = "es"): Initializes a new Text object.
            to_json(self): Converts the Text object to a JSON representation.
        """
    __tablename__ = "texts"
    # --------------------------- columnas de la tabla --------------------------- #
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content: str = db.Column(db.String(120), nullable=False)
    length: int = db.Column(db.Integer, nullable=False)
    language: str = db.Column(db.String(120), nullable=False)
    encrypted: bool = db.Column(db.Boolean, default=False)
    key: str = db.Column(db.String(120), nullable=True)
    # ------------------------------ claves foraneas ----------------------------- #
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    # ----------------------------- fin clave foranea ---------------------------- #
    # ------------------------- fin columnas de la tabla ------------------------- #
    # -------------------------------- relaciones -------------------------------- #
    histories = db.relationship("TextHistory", backref="text", lazy=True)
    # ------------------------------ fin relaciones ------------------------------ #

    def __init__(self, content: str = "default text", language: str = "es"):
        self.content = content
        self.length = len(content)
        self.language = language

    def to_json(self):
        return {
            "id": self.id,
            "content": self.content,
            "length": self.length,
            "language": self.language,
            "encrypted": self.encrypted,
            "key": self.key,
            "user_id": self.user_id,
        }
