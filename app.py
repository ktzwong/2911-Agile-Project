from flask import Flask, render_template, redirect, url_for
from pathlib import Path
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

'''links to notes'''
@app.route("/notes")
def notes_view():
    return render_template("notes.html")

if __name__ == "__main__":
     app.run(debug=True, port=8888)
