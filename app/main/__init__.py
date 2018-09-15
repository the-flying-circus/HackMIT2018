from flask import Blueprint
from . import routes, events

main = Blueprint('main', __name__)
