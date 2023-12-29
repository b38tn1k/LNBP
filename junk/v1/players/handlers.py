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
    """
    This function renders a template page with the title "Players" and displays
    two forms for adding and editing players for the current user's club: an
    AddPlayerForm and an EditPlayerForm.

    Returns:
        : The output returned by the `players()` function is a render of the
        "page-players.html" template with the following data:
        
        	- title: "Players"
        	- add_player_form: An instance of `AddPlayerForm`
        	- edit_player_form: An instance of `EditPlayerForm`
        	- club: The current user's club
        
        Note that this is a generic description and the actual output may vary
        depending on the implementation of the forms and the template.

    """
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
    """
    This function deletes a player with the given `player_id` from the database
    and returns a redirect to either the "players" page or the club page based on
    the current URL.

    Args:
        player_id (int): The `player_id` input parameter identifies the specific
            player record to be deleted.

    Returns:
        : Based on the code provided:
        
        The output returned by this function is `redirect(url_for("club.club", clubname=club.name))`.

    """
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
    """
    This function takes a `player_id` input and retrieves the corresponding `Player`
    object from the database using `Query.get_or_404()`.

    Args:
        player_id (int): The `player_id` input parameter is used to retrieve a
            specific player object from the database using the `Query.get_or_404()`
            method.

    Returns:
        : The output returned by the `edit_player()` function is a rendered HTML
        page with the title of the player's name and a list of their flights.

    """
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
    """
    This function adds or updates availability data for a specific flight of a player.

    Args:
        player_id (int): The `player_id` input parameter passes a specific player's
            ID into the add_availability() function for updating the corresponding
            availability information on that specific player record within the
            database table.

    Returns:
        dict: The output returned by this function is a JSON object with the message
        "Availability data updated successfully." if the availability data was
        updated successfully and "Invalid request data." if the request data is invalid.

    """
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
    """
    This function retrieves the availability of a player for a specific flight
    based on their previously stored availability data. If the flight ID is not
    provided or if there is no availability data for the player or the flight ID
    cannot be found , an error response will be returned.

    Args:
        player_id (int): The `player_id` input parameter identifies which player's
            availability is being queried.

    Returns:
        : Based on the given function signature and implementation:
        
        Output:
        
        	- If flight_id is provided and exists within the availability_data (as
        JSON), then return JSON with { "flight_id": <string>, "availability":
        <float> }.
        	- Otherwise:
        	+ If availability data does not exist for the specified flight_id (in
        JSON), return 404 Not Found with {"error": "Availability data not found
        for the specified flight."}.
        	+ If there is no availability data available for the player (i.e.,
        availability_data is null or empty), return 404 Not Found with {"error":
        "No availability data found for the player."}.

    """
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
