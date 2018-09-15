from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
sio = SocketIO(app)
db = SQLAlchemy(app)
lm = LoginManager(app)
