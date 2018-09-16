import requests
import functools
from pprint import pprint

from app import app, db
from flask import render_template, request, jsonify, redirect
from database import User
from flask_login import current_user, login_required

from services.secrets import GIPHY_KEY
from services.fb_data import FBService
from services.ibm_personality import PersonalityService


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html")


@app.route("/resources")
@login_required
def resources():
    return render_template("resources.html")


@app.route("/account")
@login_required
def accounts():
    return render_template("account.html")


@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/login")
def login():
    if current_user.is_anonymous:
        return render_template("login.html")
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_anonymous:
        return redirect("/login")
    elif current_user.nickname is not None and current_user.is_mentor is not None:
        return redirect("/chat")
    elif request.method == "POST":
        current_user.nickname = request.form["displayname"]
        current_user.is_mentor = request.form["role"] == "mentor"
        db.session.commit()
        return redirect("/chat")
    return render_template("register.html")


@app.route("/dbtest")
def dbtest():
    print('current user: ', current_user.social_id, current_user.access_token)
    return current_user.access_token


@app.route("/fbauthtest")
def fbtest():
    fb_service = FBService()
    posts = fb_service.get_user_posts(current_user.social_id, current_user.access_token)
    return str(posts)


@app.route("/fbibmtest")
def fbibmtest():
    fb_service = FBService()
    personality_service = PersonalityService()
    posts = fb_service.get_user_posts(current_user.social_id, current_user.access_token)
    personality = personality_service.get_personality(posts)
    pprint(personality)
    return str(personality)


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
