from db import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column


class Item(db.Model):
    __tablename__ = "items"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String)