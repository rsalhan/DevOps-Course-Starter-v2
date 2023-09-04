from todo_app.data.trello_items import add_card, todo_list, doing_list, done_list, move_to_todo, move_to_doing, move_to_done #load_lists, 

from flask import Flask, render_template, redirect
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    #load_lists()
    print('---LOADING---')
    retrieve_todo = todo_list()
    retrieve_doing = doing_list()
    retrieve_done = done_list()
    return render_template('index.html', todo_list = retrieve_todo, doing_list = retrieve_doing, done_list = retrieve_done)

@app.route('/additem', methods = ["POST"])
def add_new_item():
    add_card()
    return redirect('/')

@app.route('/movetotodo', methods = ["POST"])
def movetotodo():
    move_to_todo()
    return redirect('/')

@app.route('/movetodoing', methods = ["POST"])
def movetodoing():
    move_to_doing()
    return redirect('/')

@app.route('/movetodone', methods = ["POST"])
def movetodone():
    move_to_done()
    return redirect('/')
