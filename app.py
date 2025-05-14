from flask import Flask, render_template, redirect, url_for, request
from pathlib import Path

app = Flask(__name__)
app.instance_path = Path(" ").resolve()

# This variable temporarily stores the note in like the memory
saved_note = ""
saved_title = "" 
notes = []

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
    global saved_note, saved_title
    if request.method == "POST":
        saved_title = request.form.get("title")
        saved_note = request.form.get("note")
        return redirect(url_for("notes_view"))
    return render_template("notes.html", saved_title=saved_title, saved_note=saved_note)

@app.route("/notes-results", methods=["GET"])
def notes_results():
    query = request.args.get("search", "").lower()

    filtered_notes = [
        note for note in notes
        if query in note["title"].lower() or query in note["content"].lower()
    ] if query else []

    return render_template("notes_results.html", query=query, notes=filtered_notes)

if __name__ == "__main__":
    app.run(debug=True, port=8888)
