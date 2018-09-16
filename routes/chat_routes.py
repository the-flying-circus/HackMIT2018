from datetime import datetime
from flask import jsonify

from app import sio, db, app
from flask_login import current_user
from database import Message, Conversation, User
from sqlalchemy import or_, and_


@sio.on('send_message', '/chat')
def send_message(message, recipient):
    usr = current_user.social_id
    if usr.is_mentor:
        convo = Conversation.query().filter_by(mentor=usr, mentee=recipient).first()
    else:
        convo = Conversation.query().filter_by(mentee=recipient, mentor=usr).first()
    if convo is None:
        print('conversation not found')
        return
    timestamp = datetime.now()
    other_nick = User.query().filter_by(social_id=recipient).first()
    other_nick = other_nick.nickname
    print('message sent by {} to {} at {}: {}'.format(current_user.nickname, other_nick, timestamp, message))
    message = Message(sent=timestamp, owner=usr, recipient=recipient, contents=message)
    db.session.add(message)
    db.session.commit()


@app.route('/chat/history')
def getMessages(other):
    usr = current_user.social_id
    if usr.is_mentor:
        convo = Conversation.query().filter_by(mentor=usr, mentee=other).first()
    else:
        convo = Conversation.query().filter_by(mentee=other, mentor=usr).first()
    if convo is None:
        print('conversation not found')
        return

    messages = Message.query().filter_by(or_(and_(owner=other, recipient=usr), and_(owner=usr, recipient=other))).all()
    messages = map(lambda item: item.toDict(), messages)
    return jsonify(messages)
