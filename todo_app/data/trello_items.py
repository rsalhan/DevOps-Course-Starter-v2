import os, requests, json
from flask import request

trello_url = os.getenv("BASE_URL")
trello_key = os.getenv("API_KEY")
trello_token = os.getenv("TOKEN")

trello_board_id = os.getenv("BOARD_ID")
brainstorm_idlist = os.getenv("BRAINSTORM_IDLIST")
todo_idlist = os.getenv("TODO_IDLIST")
doing_idlist = os.getenv("DOING_IDLIST")
done_idlist = os.getenv("DONE_IDLIST")

#trello_url_params = {"key": trello_key, "token": trello_token}
headers = {"Accept": "application/json"}

# def get_member_boards():
#     get_member_boards_path = "members/me/boards?fields=name,url"
#     url = trello_url + get_member_boards_path
#     query_params = {"key": trello_key, "token": trello_token}
#     print(f"URL: {url}")
#     response = requests.get(url, headers=headers, params=query_params)
#     #response = requests.request("GET", url, headers=headers, params=query_params)
#     print(response.json())
#     return response

def get_lists():
    #id = trello_board_id
    #get_lists_path = "https://api.trello.com/1/boards/{trello_board_id}/lists"
    get_lists_path = "boards/"+trello_board_id+"/lists"
    url = trello_url + get_lists_path
    query_params = {"key": trello_key, "token": trello_token, "cards": "open", "card_fields": "id,name,shortUrl"}
    print(f"URL: {url}")
    response = requests.get(url, headers=headers, params=query_params)
    #response = requests.request("GET", url, headers=headers, params=query_params)
    print("Raw JSON response is...")
    response_json = response.json()
    print(response_json)

    cards_dict = []
    for trello_list in response_json:
        for each_card in trello_list['cards']:
            cards_dict.append(each_card)

    print("JSON (cards_dict) response is...")
    print(cards_dict)
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    return cards_dict

def add_card():
    new_todo = request.form.get('new-todo')
    add_card_path = "cards"
    url = trello_url + add_card_path
    #query_params = {"idList": '64af2a2305103833247f0e44',"key": trello_key, "token": trello_token, "name": new_todo} #, "pos": 'top'}
    query_params = {"idList": todo_idlist, "key": trello_key, "token": trello_token, "name": new_todo}
    print(f"URL: {url}")
    response = requests.request("POST", url, headers=headers, params=query_params)
    print("Raw JSON POST response is...")
    print(response.json())
    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))