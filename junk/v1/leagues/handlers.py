from flask import (
    render_template,
    jsonify,
    redirect,
    url_for,
    request,
)
from app import db
from app.leagues import bp
from app.models.flight import Flight
from app.scheduler.scheduler import Scheduler
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


@bp.route("/leagues", methods=["GET", "POST"])
@login_required
def leagues():
    """
    The `leagues()` function renders the "page-leagues.html" template and returns
    it with the `club` and 'Leagues' titles as variables.

    Returns:
        str: The output returned by the `leagues()` function is a HTML page with
        the title "Leagues".

    """
    club = current_user.club
    return render_template("page-leagues.html", club=club, title='Leagues')


@bp.route("/leagues/<int:league_id>/get_assets", methods=["GET", "POST"])
@login_required
def get_assets(league_id):
    """
    This function retrieves the scorecard and schedule of a league specified by
    the `league_id` parameter using the current user's club object and returns a
    JSON response with the status "success" and the two CSV files as content.

    Args:
        league_id (int): The `league_id` input parameter is used to specify the
            ID of the league for which the function should retrieve the assets
            (scorecard and schedule).

    Returns:
        dict: Based on the code provided:
        
        The output returned by the function is a JSON object with three keys:
        "status", "scorecard", and "schedule".

    """
    club = current_user.club
    league = club.get_league(league_id)
    scorecard = league.generate_scorecard_CSV()
    schedule = league.generate_schedule_CSV()
    return jsonify({"status": "success", "scorecard": scorecard,  "schedule": schedule}), 200

@bp.route("/leagues/<int:league_id>/generate_all", methods=["GET", "POST"])
@login_required
def generate_all(league_id):
    """
    This function generates a list of matches for a specific league based on the
    current user's club and returns a JSON object with the status "success" and a
    list of matching details.

    Args:
        league_id (int): The `league_id` input parameter specifies which league
            to retrieve and generate fixtures for.

    Returns:
        dict: The output returned by the `generate_all()` function is a JSON object
        with a single key-value pair: `"status": "success"` and a list of dictionaries
        for `"results"`.

    """
    club = current_user.club
    league = club.get_league(league_id)
    res = []
    for flight in league.flights:
        supervisor = Scheduler(flight)
        r = supervisor.generate()
        r['captained'] = supervisor.assign_captains()
        r['name'] = supervisor.flight_name
        res.append(r)
    return jsonify({"status": "success", "results":res}), 200


@bp.route("/leagues/<int:league_id>/edit", methods=["GET", "POST"])
@login_required
def edit_league(league_id):
    """
    This function edits a league given its ID by rendering a page with the league's
    information.

    Args:
        league_id (int): The `league_id` input parameter passes the ID of a specific
            league that is requested to be edited.

    Returns:
        : The output returned by the `edit_league` function is a rendered template
        named "page-league.html" with the `league` object and the title of the
        league as variables.

    """
    club = current_user.club
    league = club.get_league(league_id)
    return render_template("page-league.html", league=league, title=league.league_name)

@bp.route("/leagues/<int:league_id>/delete", methods=["GET", "POST"])
@login_required
def delete_league(league_id):
    """
    This function deletes a league with the given league ID.

    Args:
        league_id (int): The `league_id` input parameter is used to identify the
            specific league that should be deleted.

    Returns:
        : The function does not return anything because it has a `return
        jsonify({"status": "error"})` statement when the deletion fails.

    """
    print("hi")
    club = current_user.club
    league = club.get_league(league_id)
    res = league.delete()
    if res:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"})
    
@bp.route("/leagues/<int:league_id>/create-flight/<string:flight_name>", methods=["GET", "POST"])
@login_required
def create_flight(league_id, flight_name):
    """
    This function creates a new flight for a specific league with the given name
    and returns a JSON response containing the newly created flight's ID.

    Args:
        league_id (int): The `league_id` input parameter is used to identify the
            league where the flight should be created.
        flight_name (str): The `flight_name` input parameter is used to specify
            the name of the flight being created.

    Returns:
        dict: The output returned by this function is a JSON object with two
        key-value pairs: "status" and "flight_id".

    """
    club = current_user.club
    league = club.get_league(league_id)
    res = league.add_flight(flight_name)
    return jsonify({"status": "success", "flight_id": res.id})


@bp.route("/leagues/create/<string:league_name>", methods=["GET", "POST"])
@login_required
def create_league(league_name):
    """
    This function creates a new league for the current user's club and returns the
    created league's ID to the client as a JSON object.

    Args:
        league_name (str): The `league_name` input parameter is used to create a
            new league with the given name.

    Returns:
        dict: The output returned by this function is a JSON object with status
        "success" and league ID if the creation was successful; otherwise ("error"
        status with no league ID), This is based on if club has a valid league added.

    """
    club = current_user.club
    league = club.add_league(league_name)
    if league:
        return jsonify({"status": "success", "league_id": league.id})
    else:
        return jsonify({"status": "error", "league_id": "none"})

    
    # league = club.get_league(league_id)
    # return render_template(
    #         "page-league.html", league=league)
