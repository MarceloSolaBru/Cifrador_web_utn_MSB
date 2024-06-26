from typing import List
from app.models import TextHistory, Text
from app import db

class TextHistoryRepository:
    """Repository class for managing TextHistory objects in the database."""

    def save(self, text_history: TextHistory) -> TextHistory:
        """Save a TextHistory object to the database.

        Args:
            text_history (TextHistory): The TextHistory object to be saved.

        Returns:
            TextHistory: The saved TextHistory object.
        """
        db.session.add(text_history)
        db.session.commit()
        return text_history

    def delete(self, text_history: TextHistory) -> None:
        """Delete a TextHistory object from the database.

        Args:
            text_history (TextHistory): The TextHistory object to be deleted.
        """
        db.session.delete(text_history)
        db.session.commit()

    def find(self, id: int):
        """Find a TextHistory object by its ID.

        Args:
            id (int): The ID of the TextHistory object to find.

        Returns:
            TextHistory: The found TextHistory object.
        """
        return db.session.query(TextHistory).filter(TextHistory.id == id).one()

    def all(self) -> List["TextHistory"]:
        """Get all TextHistory objects from the database.

        Returns:
            List[TextHistory]: A list of all TextHistory objects.
        """
        text_histories = db.session.query(TextHistory).all()
        return text_histories

    def find_by(self, **kwargs) -> List["TextHistory"]:
        """Find TextHistory objects by keyword arguments.

        Args:
            **kwargs: Keyword arguments to filter the TextHistory objects.

        Returns:
            List[TextHistory]: A list of TextHistory objects that match the given criteria.
        """
        return db.session.query(TextHistory).filter_by(**kwargs).all()

    def change_to_version(self, text_history_id: int) -> Text:
        """Change the content of a Text object to match a TextHistory object.

        Args:
            text_history_id (int): The ID of the TextHistory object.

        Returns:
            Text: The updated Text object.
        """
        text_history = self.find(text_history_id)
        text = db.session.query(Text).filter(Text.id == text_history.text_id).one()
        text.content = text_history.content
        db.session.commit()
        return text