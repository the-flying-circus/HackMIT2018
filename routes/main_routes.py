from app import app
from flask import render_template


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


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/info")
def info():
    return render_template("info.html")
