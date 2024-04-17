import os, pymongo
from flask import request
from bson.objectid import ObjectId

def connect_to_mongo_db():
    mongo_db_connection = os.getenv("MONGO_DB_CONNECTION_STRING")
    mongo_db_name = os.getenv("MONGO_DB_NAME")
    dbclient = pymongo.MongoClient(mongo_db_connection)
    db = dbclient[mongo_db_name]
    collection = db["collection1"]
    list_collections = db.list_collection_names()

    print(f"Mongo DB CS: {mongo_db_connection}")
    print(f"Mongo DB Name: {mongo_db_name}")
    print(f"List DB names: {dbclient.list_database_names()}")
    print(f"DB: {db}")
    print(f"List collection names: {list_collections}")
    print(f"Collection: {collection}")

    return collection

class Item:
    def __init__(self, id, name, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_mongo_db(cls, card):
        return cls(card['_id'], card['name'], card['status'])

def add_card():
    collection = connect_to_mongo_db()
    new_todo = request.form.get('new-todo')
    add_todo = {"name": new_todo, "status": "To Do"}
    collection.insert_one(add_todo)

def todo_list():
    collection = connect_to_mongo_db()
    find_todo = collection.find({"status": "To Do"})
    mongo_todo = list(find_todo)

    todo_items_list = []
    for each_todoitem in mongo_todo:
        item = Item.from_mongo_db(each_todoitem)
        todo_items_list.append(item)
    return todo_items_list

def doing_list():
    collection = connect_to_mongo_db()
    find_doing = collection.find({"status": "Doing"})
    mongo_doing = list(find_doing)

    doing_items_list = []
    for each_doingitem in mongo_doing:
        item = Item.from_mongo_db(each_doingitem)
        doing_items_list.append(item)
    return doing_items_list

def done_list():
    collection = connect_to_mongo_db()
    find_done = collection.find({"status": "Done"})
    mongo_done = list(find_done)

    done_items_list = []
    for each_doneitem in mongo_done:
        item = Item.from_mongo_db(each_doneitem)
        done_items_list.append(item)
    return done_items_list

def move_to_todo():
    collection = connect_to_mongo_db()
    move_to_todo_id = request.form.get('id')
    collection.update_one({'_id': ObjectId(move_to_todo_id)}, {"$set": {"status": "To Do"}})

def move_to_doing():
    collection = connect_to_mongo_db()
    move_to_doing_id = request.form.get('id')
    collection.update_one({'_id': ObjectId(move_to_doing_id)}, {"$set": {"status": "Doing"}})

def move_to_done():
    collection = connect_to_mongo_db()
    move_to_done_id = request.form.get('id')
    collection.update_one({'_id': ObjectId(move_to_done_id)}, {"$set": {"status": "Done"}})

