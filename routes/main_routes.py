import requests
import functools

from app import app
from flask import render_template, request, jsonify

from services.secrets import GIPHY_KEY


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/resources")
def resources():
    return render_template("resources.html")


@app.route("/account")
def accounts():
    return render_template("account.html")


@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/login")
def login():
    return render_template("login.html")


@functools.lru_cache(maxsize=16)
def get_gifs(query):
    if not query:
        resp = requests.get("https://api.giphy.com/v1/gifs/trending", params={"api_key": GIPHY_KEY})
    else:
        resp = requests.get("https://api.giphy.com/v1/gifs/search", params={"api_key": GIPHY_KEY, "q": query})
    resp.raise_for_status()
    return {
        "data": [x["images"]["preview_gif"]["url"] for x in resp.json()["data"]]
    }


@app.route("/gifs")
def gifs():
    query = request.args.get("q")
    return jsonify(get_gifs(query))
