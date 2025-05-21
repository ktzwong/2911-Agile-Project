from flask import render_template, redirect, url_for, request, session, flash, jsonify, Blueprint
from pathlib import Path
from models import Note, Item
from db import db
from datetime import datetime
from sqlalchemy import select


api_bp = Blueprint("api", __name__)


# In-memory user storage
users = {}

# Home route with login/register logic
@api_bp.route("/", methods=["GET", "POST"])
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
                    return redirect(url_for("api.notes_view"))
                else:
                    error = "Incorrect password"
            else:
                users[username] = password
                session["user"] = username
                return redirect(url_for("api.notes_view"))

    return render_template("home.html",
                           error=error,
                           username_error=username_error,
                           password_error=password_error)

# Calendar page
@api_bp.route("/calendar")
def calendar_view():
    notes = db.session.execute(db.select(Note)).scalars()
    return render_template("calendar.html",notes=notes)

@api_bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    title = data.get('description')
    date_str = data.get('date')  
    note_id = data.get('note_id')

    if not title or not date_str:
        return jsonify({"error": "Missing data"}), 400
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        item = Item(title=title, date=date, note_id=note_id)
        db.session.add(item)
        db.session.commit() 
        return jsonify({"message": "Item created","note_id": note_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/items')
def get_items():
    items = db.session.execute(db.select(Item)).scalars()
    return jsonify([
        {
            "id": item.id,
            "title": item.title, 
            "start": item.date.isoformat(),
            "note_id": item.note_id
        }
        for item in items
    ])

# Notes page with database saving
@api_bp.route("/notes", methods=["GET", "POST"])
def notes_view():
    saved_title = saved_note = None
    note = None
    if "user" not in session:
        return redirect(url_for("api.home"))
    
    note_id = request.args.get("id")
    if note_id:
        try:
            note = db.session.get(Note, note_id)
            return render_template("notes.html", note=note)
        except (ValueError, TypeError):
            flash("Invalid note ID", "error")
            return redirect(url_for("api.notes_view"))
        
    if request.method == "POST":
        saved_title = request.form.get("title")
        saved_note = request.form.get("note")

        if saved_title and saved_note:
            note = Note(title=saved_title, content=saved_note)
            db.session.add(note)
            db.session.commit()
            flash("Note saved successfully!", "success")
            return redirect(url_for("api.notes_view"))
        else:
            flash("Both fields are required!", "error")

    return render_template("notes.html", saved_title=saved_title, saved_note=saved_note)

# View all notes
@api_bp.route("/all-notes")
def all_notes():
    if "user" not in session:
        return redirect(url_for("api.home"))

    notes = db.session.execute(select(Note)).scalars()
    return render_template("all_notes.html", notes=notes)

# Delete a note
@api_bp.route("/delete_note/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    note = db.session.get(Note, note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted!", "success")
    else:
        flash("Note not found.", "error")
    return redirect(url_for("api.all_notes"))

# Logout route
@api_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("api.home"))

# Search feature
@api_bp.route("/notes_results", methods=["GET"])
def notes_results():
    query = request.args.get("search", "").lower()

    if query:
        filtered_notes = Note.query.filter(
            (Note.title.ilike(f"%{query}%")) |
            (Note.content.ilike(f"%{query}%"))
        ).all()
    else:
        filtered_notes = []

    return render_template("notes_results.html", query=query, notes=filtered_notes)