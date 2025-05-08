from flask import Flask, render_template, redirect, url_for, request, session
from pathlib import Path

app = Flask(__name__)
app.instance_path = Path(" ").resolve()
app.secret_key = "secret123"  

# Simple user (can be fixed later)
USER = {"username": "student", "password": "password"}

# In-memory note storage
saved_note = ""
saved_title = ""

# Homepage with login form
@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USER["username"] and password == USER["password"]:
            session["user"] = username
            return redirect(url_for("notes_view"))
        else:
            error = "Invalid credentials"
    return render_template("home.html", error=error)

# Calendar page
@app.route("/calendar")
def calendar_view():
    return render_template("calendar.html")

# Notes page (requires login)
@app.route("/notes", methods=["GET", "POST"])
def notes_view():
    global saved_note, saved_title

    if "user" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        saved_title = request.form.get("title")
        saved_note = request.form.get("note")
        return redirect(url_for("notes_view"))

    return render_template("notes.html", saved_title=saved_title, saved_note=saved_note)

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=8888)
