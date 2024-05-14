from todo_app.data.mongo_db_items import add_card, todo_list, doing_list, done_list, move_to_todo, move_to_doing, move_to_done
from todo_app.view_model import ViewModel

from flask import Flask, render_template, redirect, url_for
from todo_app.flask_config import Config
from todo_app.oauth import blueprint
from flask_dance.contrib.github import github
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():   
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(Config())
    app.register_blueprint(blueprint, url_prefix="/login")

    @app.route('/')
    def index():
        if not github.authorized:
            return redirect(url_for("github.login"))
        print('---LOADING---')
        retrieve_todo = todo_list()
        retrieve_doing = doing_list()
        retrieve_done = done_list()
        item_view_model = ViewModel(retrieve_todo, retrieve_doing, retrieve_done)
        return render_template('index.html', view_model = item_view_model)
        #return render_template('index.html', todo_list = retrieve_todo, doing_list = retrieve_doing, done_list = retrieve_done)

    @app.route('/additem', methods = ["POST"])
    def add_new_item():
        if not github.authorized:
            return redirect(url_for("github.login"))
        add_card()
        return redirect('/')

    @app.route('/movetotodo', methods = ["POST"])
    def movetotodo():
        if not github.authorized:
            return redirect(url_for("github.login"))
        move_to_todo()
        return redirect('/')

    @app.route('/movetodoing', methods = ["POST"])
    def movetodoing():
        if not github.authorized:
            return redirect(url_for("github.login"))
        move_to_doing()
        return redirect('/')

    @app.route('/movetodone', methods = ["POST"])
    def movetodone():
        if not github.authorized:
            return redirect(url_for("github.login"))
        move_to_done()
        return redirect('/')

    return app