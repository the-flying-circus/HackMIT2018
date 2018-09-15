from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from main import app

db = SQLAlchemy(app)
lm = LoginManager(app)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)


@lm.user_loader
def load_user(key):
    return User.query.get(int(key))
