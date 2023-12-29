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
    club = current_user.club
    return render_template("page-leagues.html", club=club, title='Leagues')


@bp.route("/leagues/<int:league_id>/get_assets", methods=["GET", "POST"])
@login_required
def get_assets(league_id):
    club = current_user.club
    league = club.get_league(league_id)
    scorecard = league.generate_scorecard_CSV()
    schedule = league.generate_schedule_CSV()
    return jsonify({"status": "success", "scorecard": scorecard,  "schedule": schedule}), 200

@bp.route("/leagues/<int:league_id>/generate_all", methods=["GET", "POST"])
@login_required
def generate_all(league_id):
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
    club = current_user.club
    league = club.get_league(league_id)
    return render_template("page-league.html", league=league, title=league.league_name)

@bp.route("/leagues/<int:league_id>/delete", methods=["GET", "POST"])
@login_required
def delete_league(league_id):
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
    club = current_user.club
    league = club.get_league(league_id)
    res = league.add_flight(flight_name)
    return jsonify({"status": "success", "flight_id": res.id})


@bp.route("/leagues/create/<string:league_name>", methods=["GET", "POST"])
@login_required
def create_league(league_name):
    club = current_user.club
    league = club.add_league(league_name)
    if league:
        return jsonify({"status": "success", "league_id": league.id})
    else:
        return jsonify({"status": "error", "league_id": "none"})

    
    # league = club.get_league(league_id)
    # return render_template(
    #         "page-league.html", league=league)
