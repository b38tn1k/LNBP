from flask import Blueprint

bp = Blueprint('leagues', __name__)

from app.leagues import handlers