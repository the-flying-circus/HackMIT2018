from flask_login import UserMixin
from app import db, lm


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    access_token = db.Column(db.String(180), nullable=True, unique=True)


class Message(UserMixin, db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer(), primary_key=True)
    sent = db.Column(db.DateTime(), nullable=False)
    owner = db.Column(db.ForeignKey("user.id"), nullable=False)
    recepient = db.Column(db.ForeignKey("user.id"), nullable=False)
    contents = db.Column(db.Text(), nullable=False)


@lm.user_loader
def load_user(key):
    return User.query.get(int(key))
