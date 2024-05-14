from flask.testing import FlaskClient
import os, pytest, mongomock, pymongo
from todo_app import app
from dotenv import load_dotenv, find_dotenv
from flask_dance.consumer.storage import MemoryStorage
from todo_app.oauth import blueprint
# from flask_dance.contrib.github import github
# from pytest import MonkeyPatch

@pytest.fixture
def client(monkeypatch): #def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    storage = MemoryStorage({"access_token": "fake-token"})
    monkeypatch.setattr(blueprint, 'storage', storage)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        # Create the new app.
        test_app = app.create_app()
        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client:
            yield client

def test_index_page(client: FlaskClient):
    mongo_db_connection = os.getenv("MONGO_DB_CONNECTION_STRING")
    mongo_db_name = os.getenv("MONGO_DB_NAME")
    dbclient = pymongo.MongoClient(mongo_db_connection)
    db = dbclient[mongo_db_name]
    collection = db["collection1"]
    
    todo_1 = {"name": "Module 11", "status": "To Do"}
    todo_2 = {"name": "Module 10", "status": "Doing"}
    todo_3 = {"name": "Module 09", "status": "Done"}

    collection.insert_many([todo_1, todo_2, todo_3])
    response = client.get('/')

    assert response.status_code == 200
    assert 'Module 11' in response.data.decode()
