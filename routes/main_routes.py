import requests
import functools
from pprint import pprint

from app import app
from flask import render_template, request, jsonify
from database import User
from flask_login import current_user

from services.secrets import GIPHY_KEY
from services.fb_data import FBService
from services.ibm_personality import PersonalityService


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


@app.route("/dbtest")
def dbtest():
    print('current user: ', current_user.social_id, current_user.access_token)
    return current_user.access_token


@app.route("/fbauthtest")
def fbtest():
    fb_service = FBService()
    posts = fb_service.get_user_posts(current_user)
    return str(posts)


@app.route("/fbibmtest")
def fbibmtest():
    fb_service = FBService()
    personality_service = PersonalityService()
    posts = fb_service.get_user_posts(current_user)
    insights = personality_service.get_insights(posts)
    pprint(insights)
    return str(insights)


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
