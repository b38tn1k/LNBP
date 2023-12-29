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
    flight = Flight.query.get_or_404(flight_id)
    supervisor = Scheduler(flight)
    supervisor.generate()
    return jsonify({"status": "success"}), 200

@bp.route("/flights/<int:flight_id>/do_captains", methods=["POST"])
@login_required
def do_captains(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    supervisor = Scheduler(flight)
    supervisor.assign_captains()
    return jsonify({"status": "success"}), 200

@bp.route("/social_schedule/<int:flight_id>")
@login_required
def social_schedule(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    return render_template("page-social-schedule.html", title="Schedule Tool", flight=flight)

@bp.route("/test")
def test_console():
    return render_template("page-dev-algorithm-tests.html", title="Tests")


@bp.route("/algorithm_test", methods=["POST"])
def algorithm_test():
    # Extract the JSON payload from the request
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