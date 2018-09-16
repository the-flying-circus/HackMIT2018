from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'VERY sekr1t'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sio = SocketIO(app)
db = SQLAlchemy(app)
db.create_all()
lm = LoginManager(app)
lm.login_view = 'index'
