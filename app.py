from flask import Flask, render_template, redirect, url_for, request, jsonify
from pathlib import Path
from models import Note, Item
from db import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"
app.instance_path = Path(" ").resolve()

db.init_app(app)

'''links to homepage '''
@app.route("/")
def home():
    return render_template("home.html")

'''links to calendar'''
@app.route("/calendar")
def calendar_view():
    return render_template("calendar.html")

@app.route("/notes", methods=["GET", "POST"])
def notes_view():
    saved_title = saved_note = None

    if request.method == "POST":
        saved_title = request.form.get("title")
        saved_note = request.form.get("note")

        if saved_title and saved_note:
            note = Note(title=saved_title, content=saved_note)
            db.session.add(note)
            db.session.commit()
            return redirect(url_for("notes_view"))
        
    return render_template("notes.html", saved_title=saved_title, saved_note=saved_note)

if __name__ == "__main__":
    app.run(debug=True, port=8888)
