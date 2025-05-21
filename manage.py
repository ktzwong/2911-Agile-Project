from app import app
from db import db
from models import Note, Item

with app.app_context():
    db.drop_all()    
    db.create_all()
    print("Tables created.")