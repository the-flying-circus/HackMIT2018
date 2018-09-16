from flask import jsonify
from flask_login import current_user

from app import db, sio, app
from database import Conversation, User
from services.ibm_personality import PersonalityService


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
        involved_cons = Conversation.findWith(user.social_id)
        if len(involved_cons) >= user.max_mentees:
            continue
        invalid = True
        for con in involved_cons:
            if con.mentee == current_user.social_id:  # they're already paired
                break
        else:
            invalid = False
        # stupid way to invert for loop else
        if invalid:
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

    sio.emit('reload', room=bestMentor.social_id)

    return jsonify({"success": True})


@app.route('/isMentor')
def isMentor():
    if current_user.is_anonymous or not current_user.is_mentor:
        return 'False'
    return 'True'
