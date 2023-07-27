#import todo_app.data.session_items as module_SI
from todo_app.data.session_items import get_items, add_item
from todo_app.data.trello_items import get_lists, add_card #, get_member_boards

from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config


app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    #retrieve_items = get_items()
    retrieve_items = get_lists()
    return render_template('index.html', items_list = retrieve_items)

@app.route('/additem', methods = ["POST"])
def add_new_item():
    #new_todo = request.form.get('new-todo')
    #add_item(new_todo)
    add_card()
    return redirect('/')