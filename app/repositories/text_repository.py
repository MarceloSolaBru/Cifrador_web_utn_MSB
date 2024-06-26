from typing import List
from app.models import Text, TextHistory
from app import db


class TextRepository:
    """Repository class for managing Text objects in the database."""

    def save(self, text: Text) -> Text:
        """Save a Text object to the database.

        Args:
            text (Text): The Text object to be saved.

        Returns:
            Text: The saved Text object.
        """
        db.session.add(text)
        db.session.commit()
        return text

    def delete(self, text: Text) -> None:
        """Delete a Text object from the database.

        Args:
            text (Text): The Text object to be deleted.
        """
        db.session.delete(text)
        db.session.commit()

    def find(self, id: int):
        """Find a Text object by its ID.

        Args:
            id (int): The ID of the Text object to be found.

        Returns:
            Text: The found Text object.
        """
        return db.session.query(Text).filter(Text.id == id).one()

    def all(self) -> List["Text"]:
        """Get all Text objects from the database.

        Returns:
            List[Text]: A list of all Text objects.
        """
        texts = db.session.query(Text).all()
        return texts

    def find_by(self, **kwargs) -> List["Text"]:
        """Find Text objects by specified criteria.

        Args:
            **kwargs: Keyword arguments representing the criteria for filtering Text objects.

        Returns:
            List[Text]: A list of Text objects that match the specified criteria.
        """
        return db.session.query(Text).filter_by(**kwargs).all()

