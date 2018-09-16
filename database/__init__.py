from database.user import User
from app import db, app


def recreateDB():
    db.create_all(app=app)
