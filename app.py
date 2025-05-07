from flask import Flask, render_template, redirect, url_for, request
from pathlib import Path

app = Flask(__name__)
app.instance_path = Path(" ").resolve()

# This variable temporarily stores the note (in memory)
saved_note = ""

'''links to homepage '''
@app.route("/")
def home():
    return render_template("home.html")

'''links to calendar'''
@app.route("/calendar")
def calendar_view():
    return render_template("calendar.html")

'''links to notes'''
@app.route("/notes", methods=["GET", "POST"])
def notes_view():
    global saved_note
    if request.method == "POST":
        saved_note = request.form.get("note")
        return redirect(url_for("notes_view"))
    return render_template("notes.html", saved_note=saved_note)

if __name__ == "__main__":
    app.run(debug=True, port=8888)
