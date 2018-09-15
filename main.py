#!/usr/bin/env python3

import eventlet
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekrit'
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)
