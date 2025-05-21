import pytest
from app import app
from models import Note
from db import db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.secret_key = "testsecret"
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user"] = "student"  # Simulate login
        yield client

"""HOME TEST"""
def test_home_route(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'CalNote' in res.data

"""CALENDAR TEST"""
def test_calendar_route(client):
    res = client.get('/calendar')
    assert res.status_code == 200
    assert b'Calendar' in res.data

"""NOTES TEST"""
def test_notes_route(client):
    res = client.get('/notes')
    assert res.status_code == 200
    assert b"My Notes" in res.data

def test_notes_post_with_title_only(client):
    test_title = "Reminder"
    test_note = ""
    res = client.post("/notes", data={
        "title": test_title,
        "note": test_note
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Both fields are required!" in res.data

def test_notes_post_with_content_only(client):
    test_title = ""
    test_note = "Finish your lab!"
    res = client.post("/notes", data={
        "title": test_title,
        "note": test_note
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Both fields are required!" in res.data

def test_notes_post_with_nothing(client):
    test_title = ""
    test_note = ""
    res = client.post("/notes", data={
        "title": test_title,
        "note": test_note
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Both fields are required!" in res.data

"""VIEW ALL NOTES AND DELETE TEST""" 
def test_all_notes_route(client):
    res = client.get('/all-notes')
    assert res.status_code == 200
    assert b"All Saved Notes" in res.data

def test_notes_post_and_view_after(client):
    test_title = "hi"
    test_note = "everybody"
    with app.app_context():
        note = Note(title=test_title, content=test_note)
        db.session.add(note)
        db.session.commit()
    res = client.get('/all-notes', follow_redirects=True)
    assert res.status_code == 200
    assert b"hi" in res.data
    assert b"everybody" in res.data

def test_notes_post_and_delete_after(client):
    test_title = "Muy"
    test_note = "Importante!"
    with app.app_context():
        note = Note(title=test_title, content=test_note)
        db.session.add(note)
        db.session.commit()
        note_id = note.id
    res = client.post(f'/delete_note/{note_id}', follow_redirects=True)
    assert res.status_code == 200
    assert b"Note deleted!" in res.data

"""LOGIN AND LOGOUT TEST"""
def test_logout(client):
    res = client.get('/logout', follow_redirects=True)
    assert res.status_code == 200
    assert b"Login" in res.data

def test_notes_requires_login():
    with app.test_client() as unauth_client:
        res = unauth_client.get('/notes', follow_redirects=True)
        assert res.status_code == 200
        assert b"Login" in res.data
