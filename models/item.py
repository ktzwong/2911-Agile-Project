from db import db
from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import mapped_column, relationship


class Item(db.Model):
    __tablename__ = "items"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String)
    date = mapped_column(Date)
    note_id = mapped_column(Integer, ForeignKey('notes.id'), nullable=True)
    
    note = relationship('Note', back_populates='items')