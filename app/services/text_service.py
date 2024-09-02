from app.models import Text, TextHistory
from app.repositories import TextHistoryRepository
from app import db


class TextService:
    def edit_content(self, text: Text, new_content: str) -> Text:
        """
        Edit the content of a Text object and save the changes.

        Args:
            text (Text): The Text object to be edited.
            new_content (str): The new content to be assigned to the Text object.

        Returns:
            Text: The updated Text object.
        """
        text_history_repository = TextHistoryRepository()
        text_history = text_history_repository.save(
            TextHistory(text_id=text.id, content=text.content))
        text.content = new_content
        db.session.commit()
        return text
