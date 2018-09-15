#!/usr/bin/env python3

import eventlet
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekr1t'
socketio = SocketIO(app)


@socketio.on('echo-back')
def handle_message(client, message):
    string = 'got message "{}" from {}'.format(message, client)
    print(string)
    return string


@socketio.on('async-echo-back')
def handle_async_message(client, message):
    string = 'got message "{}" from {}'.format(message, client)
    print(string)
    sleep(5)
    emit('async back', string)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/resources")
def resources():
    return render_template("resources.html")


@app.route("/help")
def help():
    return render_template("help.html")


@app.route("/accounts")
def accounts():
    return render_template("accounts.html")


if __name__ == '__main__':
    socketio.run(app, debug=True)
