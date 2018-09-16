import random

from datetime import datetime

from flask import request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user
from sqlalchemy import or_

from app import app, db, sio
from database import User, Conversation, Message
from oauth import FacebookSignIn
from services.fb_data import FBService
from services.ibm_personality import PersonalityService


@app.route('/authorize')
def oath_authorize():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    if "bypass" in request.args:
        social_id = request.args.get("bypass")
        user = User.query.filter_by(social_id=social_id).first()
        if not user:
            personality = {
                "agreeableness": 0,
                "conscientiousness": 0,
                "emotional_range": 0,
                "extraversion": 0,
                "openness": 0
            }
            user = User(social_id=social_id, access_token="fake access token {} {}".format(datetime.now(), random.random()), max_mentees=3, **personality)
            db.session.add(user)
            db.session.commit()
        login_user(user, True)
        return redirect(url_for('register'))
    oauth = FacebookSignIn()
    return oauth.authorize()


@app.route('/auth-callback')
def oauth_callback():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    oauth = FacebookSignIn()
    social_id, access_token = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        fb_service = FBService()
        posts = fb_service.get_user_posts(social_id, access_token)
        personality_service = PersonalityService()
        personality = personality_service.get_personality(posts)
        user = User(social_id=social_id, access_token=access_token, max_mentees=3, **personality)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('register'))


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect("/")


@app.route('/destroy', methods=['POST'])
def destroy():
    Conversation.query.filter(or_(Conversation.mentor == current_user.social_id, Conversation.mentee == current_user.social_id)).delete()
    Message.query.filter(or_(Message.owner == current_user.social_id, Message.recipient == current_user.social_id)).delete()
    User.query.filter_by(social_id=current_user.social_id).delete()
    logout_user()
    db.session.commit()
    return redirect("/")
