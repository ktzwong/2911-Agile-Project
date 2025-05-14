from flask import Flask, render_template, redirect, url_for, request, session, flash
from pathlib import Path
from models import Note, Item
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"
app.secret_key = "secret123"
app.instance_path = Path(" ").resolve()

# Initialize SQLAlchemy
db.init_app(app)

# In-memory user storage
users = {}

# Home route with login/register logic
@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    username_error = None
    password_error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            username_error = "Username is required"
        if not password:
            password_error = "Password is required"
        elif len(password) < 6:
            password_error = "Password must be at least 6 characters"

        if not username_error and not password_error:
            if username in users:
                if users[username] == password:
                    session["user"] = username
                    return redirect(url_for("notes_view"))
                else:
                    error = "Incorrect password"
            else:
                users[username] = password
                session["user"] = username
                return redirect(url_for("notes_view"))

    return render_template("home.html",
                           error=error,
                           username_error=username_error,
                           password_error=password_error)

# Calendar page
@app.route("/calendar")
def calendar_view():
    return render_template("calendar.html")

# Notes page with database saving
@app.route("/notes", methods=["GET", "POST"])
def notes_view():
    saved_title = saved_note = None

    if "user" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        saved_title = request.form.get("title")
        saved_note = request.form.get("note")

        if saved_title and saved_note:
            note = Note(title=saved_title, content=saved_note)
            db.session.add(note)
            db.session.commit()
            flash("Note saved successfully!", "success")
            return redirect(url_for("notes_view"))
        else:
            flash("Both fields are required!", "error")

    return render_template("notes.html", saved_title=saved_title, saved_note=saved_note)

# Logout route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=8888)
