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
    """
    This function updates the 'fg_color' and 'bg_color' attributes of a Flight
    object with the given flight id and returns a "200" response.

    Args:
        flight_id (int): The `flight_id` input parameter is used to retrieve the
            appropriate Flight object from the database using `Flight.query.get_or_404(flight_id)`.

    Returns:
        str: Based on the code provided:
        
        The output returned by this function is "200".

    """
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
    """
    This function deletes a single flight with the specified `flight_id` from the
    database.

    Args:
        flight_id (int): The `flight_id` input parameter identifies the specific
            flight to be deleted.

    Returns:
        : The output returned by this function is JSON object with status "success".

    """
    flight = Flight.query.get_or_404(flight_id)
    flight.on_delete()
    db.session.delete(flight)
    db.session.commit()
    return jsonify({"status": "success"})


@bp.route("/flights/<int:flight_id>/timeslots/new", methods=["POST"])
@login_required
def new_time_slot(flight_id):
    """
    This function creates a new Timeslot object for a given flight ID and returns
    its ID as a JSON response.

    Args:
        flight_id (int): The `flight_id` input parameter is used to retrieve a
            Flight object from the database using `Flight.query.get_or_404()`.

    Returns:
        dict: The output returned by this function is a JSON object with the
        following fields:
        
        	- status: success
        	- timeslot_id: <the ID of the new TimeSlot>

    """
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
    """
    This function clears all events associated with a given flight ID by deleting
    them and returns a success response to the client.

    Args:
        flight_id (int): The `flight_id` input parameter identifies the flight to
            be cleared of events.

    Returns:
        tuple: The output returned by this function is JSON data with the status
        "success".

    """
    flight = Flight.query.get_or_404(flight_id)
    flight.delete_events()
    return jsonify({"status": "success"}), 200


@bp.route(
    "/flights/<int:flight_id>/timeslots/<int:timeslot_id>/edit", methods=["POST"]
)
@login_required
def update_time_slot(flight_id, timeslot_id):
    # flight = Flight.query.get_or_404(flight_id)
    """
    This function updates the start and end times of a Timeslot object with the
    given id by parsing the given start and end times as ISO strings and adjusting
    for time zone offset minutes provided as part of the request JSON.

    Args:
        flight_id (int): The `flight_id` input parameter is used to retrieve the
            corresponding flight object from the database using the
            `Flight.query.get_or_404()` method.
        timeslot_id (int): The `timeslot_id` parameter identifies which Timeslot
            instance to update based on its ID value.

    Returns:
        dict: The output returned by the function is JSON data with the status "success".

    """
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
    """
    This function deletes a Timeslot object given its id and the id of the flight
    it belongs to. If the timeslot does not belong to the specified flightId flight
    then an error message is returned with HTTP 400 Bad Request.

    Args:
        flight_id (int): The `flight_id` input parameter retrieves the flight with
            the specified ID from the database using SQLAlchemy's `query.get_or_404()`
            method before deleting the associated timeslot.
        timeslot_id (int): The `timeslot_id` input parameter specifies the ID of
            the timeslot to be deleted.

    Returns:
        str: Based on the code provided:
        
        The output returned by the function `delete_timeslot` is a JSON object
        with status "success" and message "Timeslot deleted successfully." The
        HTTP status code is 200.

    """
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
    """
    This function adds a player to a flight by inserting the player's ID into the
    flight's list of players.

    Args:
        flight_id (str): The `flight_id` input parameter specifies the ID of the
            flight to which the player should be added.

    Returns:
        dict: Based on the code provided the output returned by this function is
        JSON responses with a "status" field and either a 200 or 400 status code.
        When the player ID exists for that flight ,it returns {'error': 'Player
        is already i...', 'status': 'error'} at HTTP status 400.

    """
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
    """
    This function removes a player from a flight by identifying the relevant flight
    and player using their IDs and then removing the player from the flight's list
    of players.

    Args:
        flight_id (str): The `flight_id` input parameter identifies the specific
            flight to be modified by removing a player from it.

    Returns:
        int: Based on the code provided.

    """
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
    """
    This function retrieves all events for a given flight ID and returns them as
    a JSON response if any events are found.

    Args:
        flight_id (str): The `flight_id` input parameter is used to retrieve the
            specific Flight object that corresponds to the given ID.

    Returns:
        list: The output returned by this function is a JSON object with an "events"
        key and an empty list inside it ("[]").

    """
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
    """
    This function renders a template named "page-flight.html" with the following
    data:
    	- flight.flight_name (title)
    	- flight.get_timeslots_json() (calendar data)
    	- club.courts (list of courts)
    	- flight (the flight object)
    	- EditFlightForm ()
    	- EditPlayerForm ()

    Args:
        flight_id (int): The `flight_id` input parameter passes the ID of the
            flight to be edited into the function.

    Returns:
        : The output returned by this function is a render of the "page-flight.html"
        template with the specified variables: title (the flight name), calendar
        data (the timeslots JSON), courts (the club's courts), flight (the flight
        object), edit_flight_form (an EditFlightForm instance), and edit_player_form
        (an EditPlayerForm instance).

    """
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
