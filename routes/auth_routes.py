from flask import redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user

from app import app, db
from database import User, Conversation
from oauth import FacebookSignIn
from services.fb_data import FBService
from services.ibm_personality import PersonalityService


@app.route('/authorize')
def oath_authorize():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
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


@app.route('/whoami')
def whoami():
    if current_user.is_anonymous:
        return "You are not logged in"
    return repr(current_user)


@app.route('/pair_mentor', methods=["POST"])
def pair_mentor():
    if current_user.is_mentor:
        return jsonify({"error": "Only mentees can request pairing."})

    current_traits = {
        "agreeableness": current_user.agreeableness,
        "conscientiousness": current_user.conscientiousness,
        "emotional_range": current_user.emotional_range,
        "extraversion": current_user.extraversion,
        "openness": current_user.openness
    }

    bestMentor = None
    bestScore = 9999999999

    for user in User.query.filter_by(is_mentor=True).all():
        if len(Conversation.findWith(user.social_id)) >= user.max_mentees:
            continue

        these_traits = {
            "agreeableness": user.agreeableness,
            "conscientiousness": user.conscientiousness,
            "emotional_range": user.emotional_range,
            "extraversion": user.extraversion,
            "openness": user.openness
        }
        score = PersonalityService.get_compatibility_score(current_traits, these_traits)
        if score < bestScore:
            bestMentor = user
            bestScore = score

    if bestMentor is None:
        return jsonify({"error": "There are no mentors currently available."})

    convo = Conversation(mentee=current_user.social_id, mentor=bestMentor.social_id)
    db.session.add(convo)
    db.session.commit()
    return jsonify({"success": True})


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect("/")


@app.route('/destroy', methods=['POST'])
def destroy():
    cons = Conversation.findWith(current_user.social_id)
    for con in cons:
        con.delete()
    User.query.filter_by(social_id=current_user.social_id).delete()
    logout_user()
    db.session.commit()
    return redirect("/")
