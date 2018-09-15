#!/usr/bin/env python3

import eventlet
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekrit'
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    socketio.run(app)
