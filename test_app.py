import pytest
from app import app
from db import db
from models import Note, Item
from datetime import date

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
    res = client.get('api/')
    assert res.status_code == 200
    assert b'CalNote' in res.data



"""CALENDAR TEST"""
def test_calendar_route(client):
    res = client.get('api/calendar')
    assert res.status_code == 200
    assert b'Calendar' in res.data
    
"""NOTES TEST"""
def test_notes_route(client):
    res = client.get('api/notes')
    assert res.status_code == 200
    assert b"My Notes" in res.data
    


def test_notes_post_with_title(client):
    test_title = "Reminder"
    test_note = "Finish your lab!"
    res = client.post("api/notes", data={
        "title": test_title,
        "note": test_note
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Note saved successfully!" in res.data

def test_notes_post_with_title_only(client):
    test_title = "Reminder"
    test_note = ""
    res = client.post("api/notes", data={
        "title": test_title,
        "note": test_note
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Both fields are required!" in res.data

def test_notes_post_with_content_only(client):
    test_title = ""
    test_note = "Finish your lab!"
    res = client.post("api/notes", data={
        "title": test_title,
        "note": test_note
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Both fields are required!" in res.data

def test_notes_post_with_nothing(client):
    test_title = ""
    test_note = ""
    res = client.post("api/notes", data={
        "title": test_title,
        "note": test_note
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Both fields are required!" in res.data

#NEW
def test_all_notes_route(client):
    res = client.get('api/all-notes')
    assert res.status_code == 200
    assert b"All Saved Notes" in res.data


def test_logout(client):
    res = client.get('api/logout', follow_redirects=True)
    assert res.status_code == 200
    assert b"Login" in res.data


def test_notes_requires_login():
    with app.test_client() as unauth_client:
        res = unauth_client.get('api/notes', follow_redirects=True)
        assert res.status_code == 200
        assert b"Login" in res.data

def test_logout_redirects_home(client):
    res = client.get('api/logout', follow_redirects=True)
    assert res.status_code == 200
    assert b"Login" in res.data

def test_search_empty_query(client):
    res = client.get('api/notes_results?search=')
    assert res.status_code == 200
    assert b"No notes found for your search." in res.data


def test_search_noneexistent_note(client):
    res = client.get('api/notes_results?search=doesnotexist')
    assert res.status_code == 200

def test_create_item_success(client):
    response = client.post("api/items", json={
        "description": "Test Item",
        "date": date.today().isoformat(),
        "note_id": None
    })
    assert response.status_code == 201
    assert b"Item created" in response.data

def test_create_item_missing_data(client):
    response = client.post("api/items", json={
        "description": "", 
        "date": ""
    })
    assert response.status_code == 400
    assert b"Missing data" in response.data

def test_login():
    username = "vamos"
    password = "whitecaps"
    with app.test_client() as unauth_client:
        res = unauth_client.post('api/', data={
            "username": username,
            "password": password
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b"My Notes" in res.data

def test_login_no_username():
    username = ""
    password = "whitecaps"
    with app.test_client() as unauth_client:
        res = unauth_client.post('api/', data={
            "username": username,
            "password": password
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b"Username is required" in res.data

def test_login_no_password():
    username = "vamos"
    password = ""
    with app.test_client() as unauth_client:
        res = unauth_client.post('api/', data={
            "username": username,
            "password": password
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b"Password is required" in res.data

def test_login_invalid_password():
    username = "vamos"
    password = "white"
    with app.test_client() as unauth_client:
        res = unauth_client.post('api/', data={
            "username": username,
            "password": password
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b"Password must be at least 6 characters" in res.data

def test_login_with_nothing():
    username = ""
    password = ""
    with app.test_client() as unauth_client:
        res = unauth_client.post('api/', data={
            "username": username,
            "password": password
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b"Username is required" in res.data
        assert b"Password is required" in res.data # Making sure we see both prompts

def test_notes_post_and_view_after(client):
    test_title = "hi"
    test_note = "everybody"
    with app.app_context():
        db.drop_all() # start fresh in case this note somehow exists already LOL
        db.create_all()
        note = Note(title=test_title, content=test_note)
        db.session.add(note)
        db.session.commit()
    res = client.get('api/all-notes', follow_redirects=True)
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
    res = client.post(f'api/delete_note/{note_id}', follow_redirects=True)
    assert res.status_code == 200
    assert b"Note deleted!" in res.data