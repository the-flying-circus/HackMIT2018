#!/usr/bin/env python3

import eventlet
import requests

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit
from time import sleep
from app import app, sio

from services.secrets import GIPHY_KEY


@sio.on('echo-back')
def handle_message(client, message):
    string = 'got message "{}" from {}'.format(message, client)
    print(string)
    return string


@sio.on('async-echo-back')
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


@app.route("/account")
def accounts():
    return render_template("account.html")


@app.route("/gifs")
def gifs():
    query = request.args.get("q")
    if not query:
        resp = requests.get("https://api.giphy.com/v1/gifs/trending", params={"api_key": GIPHY_KEY})
    else:
        resp = requests.get("https://api.giphy.com/v1/gifs/search", params={"api_key": GIPHY_KEY, "q": query})
    resp.raise_for_status()
    return jsonify({
        "data": [x["images"]["preview_gif"]["url"] for x in resp.json()["data"]]
    })


if __name__ == '__main__':
    sio.run(app, debug=True)
