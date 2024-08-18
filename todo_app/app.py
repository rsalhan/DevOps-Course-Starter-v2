from todo_app.data.mongo_db_items import add_card, todo_list, doing_list, done_list, move_to_todo, move_to_doing, move_to_done
from todo_app.data.mongo_db_items import global_new_todo, global_move_to_do_id, global_move_to_doing_id, global_move_to_done_id # <<<
from todo_app.view_model import ViewModel

from flask import Flask, render_template, redirect, url_for
from todo_app.flask_config import Config
from todo_app.oauth import blueprint
from flask_dance.contrib.github import github
from werkzeug.middleware.proxy_fix import ProxyFix

import logging, os, logging.config, time, loggly.handlers
from loggly.handlers import HTTPSHandler
from logging import Formatter
# logging.config.fileConfig('python.conf')
# logging.config.fileConfig(r'C:\DevOps\M1.ProjectExercise\DevOps-Course-Starter-v2\todo_app\python.conf')
logging.Formatter.converter = time.gmtime
logger = logging.getLogger(__name__)
# logger = logging.getLogger('myLogger')

# logger.info('Test INFO')
# logger.debug('Test DEBUG')
# logger.warning('Test WARNING')
# logger.error('Test ERROR')
# logger.critical('Test CRITICAL')

def create_app():   
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(Config())
    app.register_blueprint(blueprint, url_prefix="/login")
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d %b %Y %H:%M:%S') #(filename='myapp.log',  
    log_level = os.getenv('LOG_LEVEL')
    loggly_token = os.getenv('LOGGLY_TOKEN')
    # print('LOGGLY_TOKEN: ' + loggly_token)
    app.logger.setLevel(app.config[log_level])
    app.logger.info('LOG_LEVEL: ' + log_level)

    if loggly_token is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{loggly_token}/tag/todo-app')
        # print('is not none: ' + loggly_token)
        # print(handler)
        handler.setFormatter(
            # Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
            Formatter("Date/TimeStamp: %(asctime)s | LevelName: %(levelname)s | Module: %(module)s | FileName: %(filename)s | FunctionName: %(funcName)s | LevelNo: %(levelno)s | LineNo: %(lineno)d | LoggerName: %(name)s | Message: %(message)s")
        )
        app.logger.addHandler(handler)
        

    @app.route('/')
    def index():
        if not github.authorized:
            app.logger.info('GitHub redirect/authentication required') # <<<
            return redirect(url_for("github.login"))
        print('---LOADING---')
        app.logger.info('Logged in/retrieving items...') # <<<
        retrieve_todo = todo_list()
        retrieve_doing = doing_list()
        retrieve_done = done_list()
        item_view_model = ViewModel(retrieve_todo, retrieve_doing, retrieve_done)
        app.logger.info('ViewModel retrieved items for index page') # <<<
        return render_template('index.html', view_model = item_view_model)
        #return render_template('index.html', todo_list = retrieve_todo, doing_list = retrieve_doing, done_list = retrieve_done)

    @app.route('/additem', methods = ["POST"])
    def add_new_item():
        if not github.authorized:
            app.logger.info('add_new_item(): GitHub redirect/authentication required') # <<<
            return redirect(url_for("github.login"))
        add_card()
        # app.logger.info('add_card() called') # <<<
        app.logger.info('add_card() successfully added: ' + global_new_todo()) # <<<
        return redirect('/')

    @app.route('/movetotodo', methods = ["POST"])
    def movetotodo():
        if not github.authorized:
            app.logger.info('movetodo(): GitHub redirect/authentication required') # <<<
            return redirect(url_for("github.login"))
        move_to_todo()
        # app.logger.info('move_to_do() called') # <<<
        app.logger.info('move_to_do() successfully moved ID: ' + global_move_to_do_id()) # <<<
        return redirect('/')

    @app.route('/movetodoing', methods = ["POST"])
    def movetodoing():
        if not github.authorized:
            app.logger.info('movetodoing(): GitHub redirect/authentication required') # <<<
            return redirect(url_for("github.login"))
        move_to_doing()
        # app.logger.info('move_to_doing() called') # <<<
        app.logger.info('move_to_doing() successfully moved ID: ' + global_move_to_doing_id()) # <<<
        return redirect('/')

    @app.route('/movetodone', methods = ["POST"])
    def movetodone():
        if not github.authorized:
            app.logger.info('movetodone(): GitHub redirect/authentication required') # <<<
            return redirect(url_for("github.login"))
        move_to_done()
        # app.logger.info('move_to_done() called') # <<<
        app.logger.info('move_to_done() successfully moved ID: ' + global_move_to_done_id()) # <<<
        return redirect('/')

    return app