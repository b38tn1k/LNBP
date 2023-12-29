from flask import Blueprint

bp = Blueprint('timeslots', __name__)

from app.timeslots import handlers