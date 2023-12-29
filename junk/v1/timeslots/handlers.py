from flask import (
    jsonify,
    request,
)
from app.timeslots import bp
from app.models.court import Court

from app.models.player import Player 
from app.models.timeslot import Timeslot

from flask_login import login_required

from app.utils import *
from app.CSVtools import *

@bp.route("/timeslot/<int:timeslot_id>/events/updateCaptain", methods=["POST", "GET"])
@login_required
def update_captain(timeslot_id):
    data = request.get_json()
    timeslot = Timeslot.query.get_or_404(timeslot_id)
    court_id = int(data.get("court"))
    event = timeslot.get_event_for_court_id(court_id)
    if event:
        new_captain = event.get_player_by_id(int(data.get("captain")))
        if (new_captain):
            event.update_captain(new_captain)
    return jsonify({"status": "success"}), 200


@bp.route("/timeslot/<int:timeslot_id>/events/delete", methods=["POST"])
@login_required
def delete_event(timeslot_id):
    data = request.get_json()
    timeslot = Timeslot.query.get_or_404(timeslot_id)
    court_data = data.get("court")
    timeslot.delete_event_with_court_id(int(court_data))

    return jsonify({"status": "success"}), 200


@bp.route("/timeslot/<int:timeslot_id>/events/new", methods=["POST"])
@login_required
def new_event(timeslot_id):
    data = request.get_json()
    timeslot = Timeslot.query.get_or_404(timeslot_id)
    player_data = data.get("players")
    court_data = data.get("court")
    players = [];
    for p in player_data:
        players.append(Player.query.get_or_404(int(p)))
    court = Court.query.get_or_404(int(court_data))
    timeslot.create_event(court, players)
    return jsonify({"status": "success"}), 200