import pytest
from app import app, db, Item

@pytest.fixture
def client():
    # Set up an in-memory database for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"App and Database connected successfully!" in response.data

def test_add_and_get_item(client):
    # Test adding an item (POST)
    post_response = client.post('/items', json={"name": "Test Item"})
    assert post_response.status_code == 201
    assert b"Item added!" in post_response.data

    # Test retrieving items (GET)
    get_response = client.get('/items')
    assert get_response.status_code == 200
    assert b"Test Item" in get_response.data