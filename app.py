from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from pathlib import Path
from models import Note, Item
from db import db
from datetime import datetime
from sqlalchemy import select
from routes.api import api_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"
app.secret_key = "secret123"
app.instance_path = Path(" ").resolve()

app.register_blueprint(api_bp, url_prefix="/api")

# Initialize SQLAlchemy
db.init_app(app)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=8888)