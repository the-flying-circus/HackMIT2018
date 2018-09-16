from datetime import datetime
from flask import jsonify, request

from app import sio, db, app
from flask_socketio import join_room
from flask_login import current_user
from database import Message, Conversation, User
from sqlalchemy import or_, and_


@sio.on('connect')
def on_connect():
    join_room(current_user.social_id)


@sio.on('message')
def send_message(message, recipient):
    usr = current_user.social_id
    if current_user.is_mentor:
        convo = Conversation.query.filter_by(mentor=usr, mentee=recipient).first()
    else:
        convo = Conversation.query.filter_by(mentee=usr, mentor=recipient).first()
    if convo is None:
        print('conversation not found')
        return
    timestamp = datetime.now()
    other_nick = User.query.filter_by(social_id=recipient).first()
    other_nick = other_nick.social_id
    print('message sent by {} to {} at {}: {}'.format(current_user.social_id, other_nick, timestamp, message))
    message = Message(sent=timestamp, owner=usr, recipient=recipient, contents=message)
    db.session.add(message)
    db.session.commit()

    sio.emit('message', {'sent': str(timestamp), 'owner': usr, 'recipient': recipient, 'contents': message.contents}, room=recipient)


@app.route('/chat/conversations')
def get_conversations():
    usr = current_user.social_id
    convos = Conversation.query.filter(or_(Conversation.mentor == usr, Conversation.mentee == usr)).all()
    data = []
    for conv in convos:
        other_sid = conv.mentor if conv.mentee == usr else conv.mentee
        display = User.query.filter_by(social_id=other_sid).first().nickname
        data.append({'social_id': other_sid, 'display': display})
    return jsonify({"data": data})


@app.route('/chat/history')
def getMessages():
    other = request.args.get('other')
    usr = current_user.social_id
    if current_user.is_mentor:
        convo = Conversation.query.filter_by(mentor=usr, mentee=other).first()
    else:
        convo = Conversation.query.filter_by(mentee=other, mentor=usr).first()
    if convo is None:
        return jsonify({"error": "Conversation not found!"})

    messages = Message.query.filter(
        or_(
            and_(Message.owner == other, Message.recipient == usr),
            and_(Message.owner == usr, Message.recipient == other)
        )
    ).order_by("sent").all()
    messages = list(map(lambda item: item.toDict(), messages))
    return jsonify({"data": messages, "id": usr})


@app.route('/register_conversation', methods=['POST'])
def registerConversation():
    data = request.get_json(force=True)
    other = data['other']
    usr = current_user.social_id
    if current_user.is_mentor:
        convo = Conversation(mentor=usr, mentee=other)
    else:
        convo = Conversation(mentor=other, mentee=usr)

    db.session.add(convo)
    db.session.commit()

    return 'True'


@app.route('/get_mentor', methods=['POST'])
def createMatch():
    data = request.get_json(force=True)

