# Build: 
1) `git clone https://github.com/dankvul/tg_exchange`
2) Setup virtualenv using 
`sudo pip3 install virtualenv`

3) Install virtualenv to your directory:
    `
    	virtualenv venv 
	`
4) Activate venv:
	` tg_exchange/$ source bin/venv/activate `
5) Install requirements:
	```(venv) tg_exchange/$ pip install -r requirements.txt```
6) Edit config.py, there should be vars:
```
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TGBOT_TOKEN = '<token>'
    SERVER_URL = '<server>/{}'.format(TGBOT_TOKEN)
```
7) Init db and configure flask app:
````
	(venv) tg_exchange/$ export FLASK_APP=wsgi.py
	(venv) tg_exchange/$ flask db init
	(venv) tg_exchange/$ flask db migrate
	(venv) tg_exchange/$ flask db upgrade
	(venv) tg_exchange/$ flask create_tables
````
Run
	`(venv) tg_exchange/$ gunicorn wsgi:app`

# TelegramExchange bot
This flask-app use webhook, so, you should firstly deploy source on remote server to fully run it. This app is ready to 
