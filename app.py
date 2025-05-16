from flask import Flask, render_template, redirect, url_for, request, session, flash
from pathlib import Path

app = Flask(__name__)
app.instance_path = Path(" ").resolve()
app.secret_key = "secret123"

# In-memory user and note storage
users = {}
saved_notes = []  # list of {"title": ..., "content": ...}

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

@app.route("/calendar")
def calendar_view():
    return render_template("calendar.html")

@app.route("/notes", methods=["GET", "POST"])
def notes_view():
    if "user" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        title = request.form.get("title")
        note = request.form.get("note")

        if not title or not note:
            flash("Both title and note are required!", "error")
            return redirect(url_for("notes_view"))

        saved_notes.append({"title": title, "content": note})
        flash("Note saved successfully!", "success")
        return redirect(url_for("notes_view"))

    return render_template("notes.html")

@app.route("/all-notes")
def all_notes():
    if "user" not in session:
        return redirect(url_for("home"))
    return render_template("all_notes.html", notes=saved_notes)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=8888)
