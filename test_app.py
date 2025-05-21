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
    assert b'Calendar' in res.data
    
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
    assert b"Note saved successfully!" in res.data

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

#NEW
def test_all_notes_route(client):
    res = client.get('/all-notes')
    assert res.status_code == 200
    assert b"All Saved Notes" in res.data


def test_logout(client):
    res = client.get('/logout', follow_redirects=True)
    assert res.status_code == 200
    assert b"Login" in res.data


def test_notes_requires_login():
    with app.test_client() as unauth_client:
        res = unauth_client.get('/notes', follow_redirects=True)
        assert res.status_code == 200
        assert b"Login" in res.data

def test_logout_redirects_home(client):
    res = client.get('/logout', follow_redirects=True)
    assert res.status_code == 200
    assert b"Login" in res.data

def test_search_empty_query(client):
    res = client.get('/notes_results?search=')
    assert res.status_code == 200
    assert b"No notes found for your search." in res.data


def test_search_noneexistent_note(client):
    res = client.get('/notes_results?search=doesnotexist')
    assert res.status_code == 200