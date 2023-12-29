from flask import (
    render_template,
    jsonify,
    redirect,
    url_for,
    request,
)
from app import db
from app.players import bp
from app.models.flight import Flight
from app.models.player import Player 
from app.forms import (
    AddPlayerForm,
    EditPlayerForm,
)
from flask_login import current_user, login_required

import json
from app.utils import *
from app.CSVtools import *

@bp.route("/players", methods=["GET", "POST"])
@login_required
def players():
    club = current_user.club
    apf = AddPlayerForm()
    epf = EditPlayerForm()
    if apf.validate_on_submit():
        club.add_player(apf.player_name.data, apf.player_email.data)
        apf.player_name.data = ""
        apf.player_email.data = ""
        db.session.commit()
    return render_template(
        "page-players.html",
        title="Players",
        add_player_form=apf,
        edit_player_form=epf,
        club=club,
    )


@bp.route("/players/<int:player_id>/delete", methods=["POST"])
@login_required
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    if "players" in request.referrer:
        return redirect(url_for("players.players"))
    else:
        return redirect(url_for("club.club", clubname=club.name))


@bp.route("/players/<int:player_id>/edit", methods=["POST"])
@login_required
def edit_player(player_id):
    player = Player.query.get_or_404(player_id)
    print("FLIGHTS")
    for f in player.flights:
        print(f)
    return render_template(
        "page-player.html", title=player.player_name, player=player
    )

@bp.route("/players/<int:player_id>/addAvailability", methods=["POST"])
@login_required
def add_availability(player_id):
    # Check if the current user is logged in and authorized to perform the action

    # Get the player from the database
    player = Player.query.get_or_404(player_id)

    # Get the availability data from the request (assuming the data is sent as JSON in the request body)
    data = request.get_json()

    # Update the player's availability_data with the new availability information
    if "flight_id" in data and "availability" in data:
        flight_id = data["flight_id"]
        availability = data["availability"]
        flight = Flight.query.get(flight_id)

        # Make sure the player is part of the specified flight (optional check)
        if not flight.player_in_flight(player):
            return jsonify({"error": "Player is not part of the specified flight."}), 400

        # Load the existing availability data (if any)
        availability_data = {}
        if player.availability_data:
            availability_data = json.loads(player.availability_data)

        # Update or add the availability for the specified flight
        availability_data[str(flight_id)] = availability

        # Save the updated availability data to the player's availability_data column
        player.availability_data = json.dumps(availability_data)
        db.session.commit()

        return jsonify({"message": "Availability data updated successfully."}), 200
    else:
        return jsonify({"error": "Invalid request data."}), 400
    
@bp.route("/players/<int:player_id>/getAvailability", methods=["GET"])
@login_required
def get_availability(player_id):
    # Check if the current user is logged in and authorized to perform the action

    # Get the player from the database
    player = Player.query.get_or_404(player_id)

    # Get the flight_id from the query parameters (assuming it's passed as a query parameter)
    flight_id = request.args.get("flight_id")

    # If the flight_id is not provided, return an error
    if not flight_id:
        return jsonify({"error": "Missing flight_id parameter."}), 400

    # Load the availability data (if any)
    if player.availability_data:
        availability_data = json.loads(player.availability_data)
        # Get the availability for the specified flight_id
        availability = availability_data.get(str(flight_id))
        if availability is not None:
            return jsonify({"flight_id": flight_id, "availability": availability}), 200
        else:
            return jsonify({"error": "Availability data not found for the specified flight."}), 404
    else:
        return jsonify({"error": "No availability data found for the player."}), 404
