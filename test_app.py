import pytest
from app import app 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_calendar_route(client):
    res = client.get('/calendar')
    assert res.status_code == 200
    assert b'Calendar' in res.data