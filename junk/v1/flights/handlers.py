from flask import (
    render_template,
    jsonify,
    redirect,
    url_for,
    request,
)
from app import db
from app.flights import bp
from app.models.court import Court
from app.models.flight import Flight
from app.models.player import Player 
from app.models.timeslot import Timeslot
from app.forms import (
    AddFlightForm,
    EditFlightForm,
    EditPlayerForm,
)
from flask_login import current_user, login_required
from datetime import timedelta

from dateutil.parser import isoparse
from app.utils import *
from app.CSVtools import *


@bp.route("/flights/<int:flight_id>/colors", methods=["POST"])
@login_required
def update_colors(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    fg_color = request.form.get("fgcolor")
    bg_color = request.form.get("bgcolor")

    if fg_color and bg_color:
        flight.fg_color = fg_color
        flight.bg_color = bg_color
        db.session.commit()

    return "200"

@bp.route("/flights/<int:flight_id>/delete", methods=["POST"])
@login_required
def delete_flight(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    flight.on_delete()
    db.session.delete(flight)
    db.session.commit()
    return jsonify({"status": "success"})


@bp.route("/flights/<int:flight_id>/timeslots/new", methods=["POST"])
@login_required
def new_time_slot(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    data = request.get_json()
    courts = []
    for i in data["courts"]:
        court = Court.query.get(i)
        if court is not None:
            courts.append(court)

    # Convert 'start' and 'end' from ISO strings to Python datetime objects with time zone info
    start = isoparse(data["start"])
    end = isoparse(data["end"])
    # Adjust start and end datetime objects based on the time zone offset
    time_zone_offset_minutes = data["timeZoneOffset"]
    start = start - timedelta(minutes=time_zone_offset_minutes)
    end = end - timedelta(minutes=time_zone_offset_minutes)

    tsid = flight.create_timeslot(start, end, courts)
    # Return a success response with the ID of the new TimeSlot
    return jsonify({"status": "success", "timeslot_id": tsid})

@bp.route("/flights/<int:flight_id>/clear", methods=["POST"])
@login_required
def clear_schedule(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    flight.delete_events()
    return jsonify({"status": "success"}), 200


@bp.route(
    "/flights/<int:flight_id>/timeslots/<int:timeslot_id>/edit", methods=["POST"]
)
@login_required
def update_time_slot(flight_id, timeslot_id):
    # flight = Flight.query.get_or_404(flight_id)
    timeslot = Timeslot.query.get_or_404(timeslot_id)
    data = request.get_json()
    start = isoparse(data["start"])
    end = isoparse(data["end"])
    time_zone_offset_minutes = data["timeZoneOffset"]
    start = start - timedelta(minutes=time_zone_offset_minutes)
    end = end - timedelta(minutes=time_zone_offset_minutes)
    timeslot.start_time = start
    timeslot.end_time = end
    db.session.commit()
    return jsonify({"status": "success"})


@bp.route(
    "/flights/<int:flight_id>/timeslots/<int:timeslot_id>/delete", methods=["DELETE"]
)
@login_required
def delete_timeslot(flight_id, timeslot_id):
    flight = Flight.query.get_or_404(flight_id)
    timeslot = Timeslot.query.get_or_404(timeslot_id)
    # Ensure that the timeslot belongs to the specified flight
    if timeslot.flight_id != flight.id:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Timeslot does not belong to the specified flight.",
                }
            ),
            400,
        )

    # Delete the timeslot
    db.session.delete(timeslot)
    db.session.commit()

    return (
        jsonify({"status": "success", "message": "Timeslot deleted successfully."}),
        200,
    )


@bp.route("/flights/<int:flight_id>/players/add", methods=["POST"])
@login_required
def add_player_to_flight(flight_id):
    data = request.get_json()
    player_id = data.get("player_id")

    if not player_id:
        return jsonify({"error": "Missing player_id parameter"}), 400

    flight = Flight.query.get_or_404(flight_id)
    player = Player.query.get_or_404(player_id)

    if flight not in player.flights:
        flight.players.append(player)
        db.session.commit()
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Player is already in the flight"}), 400


@bp.route("/flights/<int:flight_id>/players/remove", methods=["POST"])
@login_required
def remove_player_from_flight(flight_id):
    data = request.get_json()
    player_id = data.get("player_id")

    if not player_id:
        return jsonify({"error": "Missing player_id parameter"}), 400

    flight = Flight.query.get_or_404(flight_id)
    player = Player.query.get_or_404(player_id)

    if flight in player.flights:
        flight.players.remove(player)
        db.session.commit()
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Player is not in the flight"}), 400
    
@bp.route("/flights/<int:flight_id>/events/get", methods=["POST"])
@login_required
def get_events(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    if flight:
        events = flight.get_events()
        if events:
            return jsonify({"events": events})
        else:
            return jsonify({"events": []})
    else:
        return jsonify({"error": "Player is not in the flight"}), 400

@bp.route("/flights/<int:flight_id>/edit", methods=["GET", "POST"])
@login_required
def edit_flight(flight_id):
    club = current_user.club
    flight = Flight.query.get_or_404(flight_id)
    elf = EditFlightForm()
    epf = EditPlayerForm()
    return render_template(
        "page-flight.html",
        title=flight.flight_name,
        calendar_data=flight.get_timeslots_json(),
        courts=club.courts,
        flight=flight,
        edit_flight_form=elf,
        edit_player_form=epf,
    )
