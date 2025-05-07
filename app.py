<<<<<<< HEAD
from flask import Flask, render_template, redirect, url_for, request
from pathlib import Path

app = Flask(__name__)
app.instance_path = Path(" ").resolve()

# This variable temporarily stores the note (in memory)
saved_note = ""
=======
from flask import Flask, render_template, redirect, url_for
from pathlib import Path
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"
app.instance_path = Path(" ").resolve()


db.init_app(app)
>>>>>>> development

'''links to homepage '''
@app.route("/")
def home():
    return render_template("home.html")

'''links to calendar'''
@app.route("/calendar")
def calendar_view():
    return render_template("calendar.html")

'''links to notes'''
<<<<<<< HEAD
@app.route("/notes", methods=["GET", "POST"])
def notes_view():
    global saved_note
    if request.method == "POST":
        saved_note = request.form.get("note")
        return redirect(url_for("notes_view"))
    return render_template("notes.html", saved_note=saved_note)

if __name__ == "__main__":
    app.run(debug=True, port=8888)
=======
@app.route("/notes")
def notes_view():
    return render_template("notes.html")

if __name__ == "__main__":
     app.run(debug=True, port=8888)
>>>>>>> development
