from db import db
from sqlalchemy import Integer, String,Text
from sqlalchemy.orm import mapped_column


class Note(db.Model):
    __tablename__ = "notes"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String)
    content = mapped_column(Text)

    
    def to_json(self):
        return {"id": self.id, 
                "title": self.title, 
                "content": self.content}