import pytest
from app import app

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
    assert b'CalNote' in res.data

"""NOTES TEST"""
def test_notes_route(client):
    res = client.get('/notes')
    assert res.status_code == 200
    assert b"My Notes" in res.data

def test_notes_post_with_title(client):
    test_title = "Reminder"
    test_note = "Finish your lab!"
    res = client.post("/notes", data={
        "title": test_title,
        "note": test_note
    }, follow_redirects=True)
    assert res.status_code == 200
    assert test_title.encode() in res.data
    assert test_note.encode() in res.data
