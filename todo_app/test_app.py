import os, pytest, requests
from todo_app import app
from dotenv import load_dotenv, find_dotenv

@pytest.fixture
def client():

    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data
    
# Stub replacement for requests.get(url)
def stub(action, url, headers={}, params={}):
    test_todo_id = os.environ.get('TODO_IDLIST')
    test_doing_id = os.environ.get('DOING_IDLIST')
    test_done_id = os.environ.get('DONE_IDLIST')
    fake_response_data = None
    
    #test_board_id = os.environ.get('TRELLO_BOARD_ID')

    # if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
    #     fake_response_data = [{
    #         'id': '123abc',
    #         'name': 'To Do',
    #         'cards': [{'id': '456', 'name': 'ToDo test card'}]
    #     },{'id': '456def',
    #         'name': 'Doing',
    #         'cards': [{'id': '789', 'name': 'Doing test card'}]
    #     },{'id': '789ghi',
    #         'name': 'Done',
    #         'cards': [{'id': '101112', 'name': 'Done test card'}]
    #     }]
    #     return StubResponse(fake_response_data)
    
    if url == f'https://api.trello.com/1/lists/{test_todo_id}/cards':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '456', 'name': 'ToDo test card'}]
        }]
        return StubResponse(fake_response_data)
       
    if url == f'https://api.trello.com/1/lists/{test_doing_id}/cards':
        fake_response_data = [{
            'id': '456def',
            'name': 'Doing',
            'cards': [{'id': '789', 'name': 'Doing test card'}]
        }]
        return StubResponse(fake_response_data)
    
    if url == f'https://api.trello.com/1/lists/{test_done_id}/cards':
        fake_response_data = [{
            'id': '789ghi',
            'name': 'Done',
            'cards': [{'id': '101112', 'name': 'Done test card'}]
        }]
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')

def test_index_page(monkeypatch, client):
    # Replace requests.get(url) with our own function
    # monkeypatch.setattr(requests, 'get', stub)
    monkeypatch.setattr(requests, 'request', stub)
    # monkeypatch.setattr(requests.request, 'get', stub)
    # monkeypatch.setattr(trello_items, 'get', stub)

    # Make a request to our app's index page
    response = client.get('/')

    assert response.status_code == 200
    # assert 'Test card' in response.data.decode()
    # assert 'ToDo test card' in response.data.decode()
    assert 'To Do' in response.data.decode()
    assert '123abc' in response.data.decode()





