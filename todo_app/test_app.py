from flask.testing import FlaskClient
import os, pytest, requests, mongomock, pymongo
from todo_app import app
from dotenv import load_dotenv, find_dotenv

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

    # # Create the new app.
    # test_app = app.create_app()

    # # Use the app to create a test_client that can be used in our tests.
    # with test_app.test_client() as client:
    #     yield client


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

    # Make a request to our app's index page
    response = client.get('/')

    assert response.status_code == 200
    assert 'Module 11' in response.data.decode()
    # assert 'Module 11' in response.data

