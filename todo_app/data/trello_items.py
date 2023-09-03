import os, requests
from flask import request

def trello_url():
    return os.getenv("BASE_URL")

def trello_key():
    return os.getenv("API_KEY")

def trello_token():
    return os.getenv("TOKEN")

def trello_board_id():
    return os.getenv("BOARD_ID")

# trello_url = os.getenv("BASE_URL")
# trello_key = os.getenv("API_KEY")
# trello_token = os.getenv("TOKEN")
# trello_board_id = os.getenv("BOARD_ID")

headers = {"Accept": "application/json"}

get_lists_path = "boards/"+trello_board_id()+"/lists"
url = trello_url() + get_lists_path
query_params = {"key": trello_key(), "token": trello_token(), "field": "name"}
print(f"--> URL: {url}")
response = requests.request("GET", url, headers=headers, params=query_params)
response_json = response.json()
print(response_json)

todo_idlist = response_json[0].get("id")
doing_idlist = response_json[1].get("id")
done_idlist = response_json[2].get("id")

def add_card():
    new_todo = request.form.get('new-todo')
    add_card_path = "cards"
    url = trello_url() + add_card_path
    query_params = {"idList": todo_idlist, "key": trello_key(), "token": trello_token(), "name": new_todo}
    print(f"--> add_card URL: {url}")
    add_card_response = requests.request("POST", url, headers=headers, params=query_params)
    add_card_json = add_card_response.json()
    print(add_card_json)

def todo_list():
    todo_list_path = "lists/"+todo_idlist+"/cards"
    todo_url = trello_url() + todo_list_path
    query_params = {"key": trello_key(), "token": trello_token(), "fields": "name"}
    print(f"--> todo_list URL: {todo_url}")
    todo_response = requests.request("GET", todo_url, headers=headers, params=query_params)
    todo_json = todo_response.json()
    print(todo_json)
    return todo_json

def doing_list():
    doing_list_path = "lists/"+doing_idlist+"/cards"
    doing_url = trello_url() + doing_list_path
    query_params = {"key": trello_key(), "token": trello_token(), "fields": "name"}
    print(f"--> doing_list URL: {doing_url}")
    doing_response = requests.request("GET", doing_url, headers=headers, params=query_params)
    doing_json = doing_response.json()
    print(doing_json)
    return doing_json

def done_list():
    done_list_path = "lists/"+done_idlist+"/cards"
    done_url = trello_url() + done_list_path
    query_params = {"key": trello_key(), "token": trello_token(), "fields": "name"}
    print(f"--> done_list URL: {done_url}")
    done_response = requests.request("GET", done_url, headers=headers, params=query_params)
    done_json = done_response.json()
    print(done_json)
    return done_json

def move_to_todo():
    trello_card_id = request.form.get('id')
    move_to_todo_path = "cards/" + trello_card_id
    move_to_todo_url = trello_url() + move_to_todo_path
    query_params = {"idList": todo_idlist, "key": trello_key(), "token": trello_token(), "pos" : 'bottom'}
    print(f"--> MoveToToDo URL: {move_to_todo_url}")
    requests.request("PUT", move_to_todo_url, headers=headers, params=query_params)

def move_to_doing():
    trello_card_id = request.form.get('id')
    move_to_doing_path = "cards/" + trello_card_id
    move_to_doing_url = trello_url() + move_to_doing_path
    query_params = {"idList": doing_idlist, "key": trello_key(), "token": trello_token(), "pos" : 'bottom'}
    print(f"--> MoveToDoing URL: {move_to_doing_url}")
    requests.request("PUT", move_to_doing_url, headers=headers, params=query_params)

def move_to_done():
    trello_card_id = request.form.get('id')
    move_to_done_path = "cards/" + trello_card_id
    move_to_done_url = trello_url() + move_to_done_path
    query_params = {"idList": done_idlist, "key": trello_key(), "token": trello_token(), "pos" : 'bottom'}
    print(f"--> MoveToDone URL: {move_to_done_url}")
    requests.request("PUT", move_to_done_url, headers=headers, params=query_params)

