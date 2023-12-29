from flask import (
    render_template,
    jsonify,
    request,
)

from app.models.flight import Flight

from .scheduler import Scheduler

from flask_login import current_user, login_required
from app.scheduler import bp

from itertools import product
from app.utils import *
from app.CSVtools import *

@bp.route("/flights/<int:flight_id>/generate", methods=["POST"])
@login_required
def generate_schedule(flight_id):
    """
    This function generates a schedule for a specific flight using the `Scheduler`
    class and returns a JSON response indicating success.

    Args:
        flight_id (str): The `flight_id` input parameter is used to retrieve a
            specific Flight object from the database using the `Flight.query.get_or_404()`
            method.

    Returns:
        tuple: The output returned by the function is JSON data with a status of
        "success".

    """
    flight = Flight.query.get_or_404(flight_id)
    supervisor = Scheduler(flight)
    supervisor.generate()
    return jsonify({"status": "success"}), 200

@bp.route("/flights/<int:flight_id>/do_captains", methods=["POST"])
@login_required
def do_captains(flight_id):
    """
    This function assigns captains to a flight using a scheduling algorithm and
    returns a JSON response with the status "success".

    Args:
        flight_id (str): The `flight_id` input parameter is used to retrieve the
            Flight object from the database using `Flight.query.get_or_404(flight_id)`,
            allowing the function to proceed only if a flight with the specified
            ID exists.

    Returns:
        dict: The output returned by this function is a JSON object with a single
        key-value pair: {"status": "success"} , accompanied by a HTTP status code
        of 200 .

    """
    flight = Flight.query.get_or_404(flight_id)
    supervisor = Scheduler(flight)
    supervisor.assign_captains()
    return jsonify({"status": "success"}), 200

@bp.route("/social_schedule/<int:flight_id>")
@login_required
def social_schedule(flight_id):
    """
    This function retrieves a Flight object with the specified id using
    Flight.query.get_or_404() and then renders a template page-social-schedule.html
    with the flight data as its variable flight.

    Args:
        flight_id (int): The `flight_id` input parameter retrieves a specific
            flight from the database using `Flight.query.get_or_404()` method and
            passes it to the template page for display.

    Returns:
        : The output returned by the `social_schedule` function is an HTML page
        rendered with the template "page-social-schedule.html".

    """
    flight = Flight.query.get_or_404(flight_id)
    return render_template("page-social-schedule.html", title="Schedule Tool", flight=flight)

@bp.route("/test")
def test_console():
    """
    This function renders a template named "page-dev-algorithm-tests.html" and
    returns the resulting HTML page with the title "Tests".

    Returns:
        : The output returned by the function `test_console()` is an HTML page
        with a title of "Tests".

    """
    return render_template("page-dev-algorithm-tests.html", title="Tests")


@bp.route("/algorithm_test", methods=["POST"])
def algorithm_test():
    # Extract the JSON payload from the request
    """
    This function takes a JSON payload with the following parameters:
    	- "players": a range of values for the number of players
    	- "courts": a range of values for the number of courts
    	- "timeslots": a range of values for the number of timeslots
    	- "days": a range of values for the number of days
    	- "weeks": a range of values for the number of weeks
    	- "iterations": an integer representing the number of iterations to perform
    It then extracts each parameter value and uses the `product` function to
    generate all possible combinations of these values. It then tests each combination
    by creating a supervisor object with those parameters and using the `testMode`
    method to simulate the schedule generation process.

    Returns:
        dict: Based on the code provided:
        
        The output returned by this function is a JSON array of dictionaries where
        each dictionary represents a combination of values for players/timeslots/courts/days/weeks
        and their corresponding result.

    """
    data = request.get_json()

    # Unpack the data
    players_values = range(data["players"][0], data["players"][1] + 1)
    courts_values = range(data["courts"][0], data["courts"][1] + 1)
    timeslots_values = range(data["timeslots"][0], data["timeslots"][1] + 1)
    days_values = range(data["days"][0], data["days"][1] + 1)
    weeks_values = range(data["weeks"][0], data["weeks"][1] + 1)
    iterations_value = data["iterations"]

    # Get all combinations
    combinations = list(product(players_values, courts_values, timeslots_values, days_values, weeks_values))

    # Convert combinations to a list of dictionaries for readability
    combinations_dicts = []
    for combo in combinations:
        combinations_dicts.append({
            "players": combo[0],
            "courts": combo[1],
            "timeslots": combo[2],
            "days": combo[3],
            "weeks": combo[4],
        })

    analysis = []
    for c in combinations_dicts:
        supervisor = Scheduler(None)
        supervisor.testMode(c["players"], c["timeslots"], c["courts"], c["days"], c["weeks"], iterations_value)
        c['result'] = supervisor.generate()

    # Return a response
    return jsonify(combinations_dicts)