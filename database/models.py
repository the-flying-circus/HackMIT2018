from flask_login import UserMixin
from sqlalchemy import or_

from app import db, lm


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=True)
    access_token = db.Column(db.String(180), nullable=True, unique=True)
    is_mentor = db.Column(db.Boolean(), nullable=True)
    max_mentees = db.Column(db.Integer(), nullable=False, default=3)

    agreeableness = db.Column(db.Float(), nullable=False)
    conscientiousness = db.Column(db.Float(), nullable=False)
    emotional_range = db.Column(db.Float(), nullable=False)
    extraversion = db.Column(db.Float(), nullable=False)
    openness = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return 'User(id={}, social_id={}, nickname={}, is_mentor={}, access_token={})'.format(self.id, self.social_id, self.nickname, self.is_mentor, self.access_token)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer(), primary_key=True)
    sent = db.Column(db.DateTime(), nullable=False)
    owner = db.Column(db.ForeignKey("users.social_id"), nullable=False)
    recipient = db.Column(db.ForeignKey("users.social_id"), nullable=False)
    contents = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return 'Message(id={}, sent={}, owner={}, recipient={}, contents={})'.format(self.id, self.sent, self.owner, self.recipient, self.contents)

    def toDict(self):
        return {'timestamp': self.sent, 'sender': self.owner, 'recipient': self.recipient, 'message': self.contents}


class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer(), primary_key=True)
    mentor = db.Column(db.ForeignKey("users.social_id"), nullable=False)
    mentee = db.Column(db.ForeignKey("users.social_id"), nullable=False)

    def __repr__(self):
        return 'Conversation(id={}, mentor={}, mentee={})'.format(self.id, self.mentor, self.mentee)

    @staticmethod
    def findWith(user):
        # finds all the conversations involving a user
        return Conversation.query.filter(or_(Conversation.mentor == user, Conversation.mentee == user)).all()


@lm.user_loader
def load_user(key):
    return User.query.get(int(key))
