import os, pytest, requests, mongomock, pymongo
from todo_app import app
from dotenv import load_dotenv, find_dotenv

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
    # Create the new app.
        test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client:
            yield client

# class StubResponse():
#     def __init__(self, fake_response_data):
#         self.fake_response_data = fake_response_data

#     def json(self):
#         return self.fake_response_data
    
# Stub replacement for requests.get(url)
# def stub(action, url, headers={}, params={}):
#     test_todo_id = os.environ.get('TODO_IDLIST')
#     test_doing_id = os.environ.get('DOING_IDLIST')
#     test_done_id = os.environ.get('DONE_IDLIST')
#     fake_response_data = None
        
#     if url == f'https://api.trello.com/1/lists/{test_todo_id}/cards':
#         fake_response_data = [
#             {'id': '123', 'name': 'ToDo test card 1'},
#             {'id': '456', 'name': 'ToDo test card 2'}
#             ]
#         return StubResponse(fake_response_data)
       
#     if url == f'https://api.trello.com/1/lists/{test_doing_id}/cards':
#         fake_response_data = [
#             {'id': '789', 'name': 'Doing test card'}
#             ]
#         return StubResponse(fake_response_data)
    
#     if url == f'https://api.trello.com/1/lists/{test_done_id}/cards':
#         fake_response_data = [
#             {'id': '101112', 'name': 'Done test card'}
#             ]
#         return StubResponse(fake_response_data)

#     raise Exception(f'Integration test did not expect URL "{url}"')

# def test_index_page(monkeypatch, client):
    # Replace requests.get(url) with our own function
    # monkeypatch.setattr(requests, 'request', stub)

def test_index_page(monkeypatch, client):
    mongo_db_connection = os.getenv("MONGOMOCK_DB_CONNECTION_STRING")
    mongo_db_name = os.getenv("MONGOMOCK_DB_NAME")
    client = pymongo.MongoClient(mongo_db_connection)
    db = client[mongo_db_name]
    collection = db["collection1"]
    # list_collections = db.list_collection_names()

    todo_1 = {
        "name": "Module 11",
        "status": "To Do"
    }

    todo_2 = {
        "name": "Module 10",
        "status": "Doing"
    }

    todo_3 = {
        "name": "Module 9",
        "status": "Done"
    }

    collection.insert_many([todo_1, todo_2, todo_3])

    # Make a request to our app's index page
    response = client.get('/')

    assert response.status_code == 200
    # assert 'ToDo test card 2' in response.data.decode()
    assert 'Module 11' in response.data.decode()

