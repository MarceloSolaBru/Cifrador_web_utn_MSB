from typing import List
from app.models import Text, TextHistory
from app import db


class TextRepository:
    def save(self, text: Text) -> Text:
        db.session.add(text)
        db.session.commit()
        return text

    def delete(self, text: Text) -> None:
        db.session.delete(text)
        db.session.commit()

    def find(self, id: int):
        return db.session.query(Text).filter(Text.id == id).one()

    def all(self) -> List["Text"]:
        texts = db.session.query(Text).all()
        return texts

    def find_by(self, **kwargs) -> List["Text"]:
        return db.session.query(Text).filter_by(**kwargs).all()

    def change_to_version(self, text_id:int)->Text:
        text_history=TextRepository.find(self,text_id)
        db.session.add(text_history)
        db.session.commit()
        return text_history