from flask import Flask
from .webhook import webhook
from config import Config
from .bot_menu import start_bot
from .extensions import db, migrate
from .utils import create_tables
from .controller import list_of_rates


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    app.cli.add_command(create_tables)
    #start_bot()
    app.register_blueprint(webhook)
    return app



