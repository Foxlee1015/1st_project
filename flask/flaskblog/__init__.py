# __init__.py -> 파이썬에게 이게 들어있는 폴더(flaskblog)는 패키지다
from flask import Flask  # render - return 으로 해당 html 나옴 // url_for 템플릿 {{ url_for('home')}} (/home) 아님 // flash - like a popup // redirect(url_for('about') 이동
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '50174397'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from flaskblog import routes
