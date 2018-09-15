#!/usr/bin/env python3

import eventlet
import requests

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit
from time import sleep
from app import app, sio
from routes import sio_test_routes, main_routes

from services.secrets import GIPHY_KEY


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
