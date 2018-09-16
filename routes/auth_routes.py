from flask import redirect, url_for, flash
from flask_login import current_user, login_user

from app import app, db
from oauth import FacebookSignIn
from database import User
from services.fb_data import FBService
from services.ibm_personality import PersonalityService


@app.route('/authorize')
def oath_authorize():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oath = FacebookSignIn()
    return oath.authorize()


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
        user = User(social_id=social_id, access_token=access_token, **personality)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


@app.route('/whoami')
def whoami():
    if current_user.is_anonymous:
        return "You are not logged in"
    return repr(current_user)
