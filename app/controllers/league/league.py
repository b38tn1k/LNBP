from flask import (
    Blueprint,
    render_template,
    abort,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
)
from flask_login import login_required, current_user
from app.forms import SimpleForm
from app.forms.club_forms import ClubSetup, FacilitySetup
from app.models import db
from app.models.clubs import Club, Facility
from app.services.league_services import (
    league_wizard_csv_to_dicts,
    build_league_from_json,
    apply_edits,
    create_games_from_request,
)
from app.services.scheduler import Scheduler
import json

blueprint = Blueprint("league", __name__)

from app.mailers.notification import NotificationMailer


@blueprint.before_request
def check_for_membership(*args, **kwargs):
    # Ensure that anyone that attempts to pull up the dashboard is currently an active member
    """
    This function checks if the current user is an active member and if they have
    access to the dashboard.

    Returns:
        None: The function returns `Redirect(url_for("main.home"))`, which is a
        HTTP redirection to the "home" view.

    """
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        flash("You currently do not have accesss to app", "warning")
        return redirect(url_for("main.home"))


@blueprint.route("/<int:id>", methods=["GET", "POST"])
@login_required
def league_home(id):
    """
    This function named `edit_league` redirects the user to the home page if they
    don't have access or if the specified league doesn't exist.

    Args:
        id (int): The `id` input parameter is used to identify the specific League
            object to be edited.

    Returns:
        str: The output returned by this function is a rendered HTML template
        called "league/edit.html" with the "league" variable set to the league
        object retrieved by the current user's club.

    """
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        flash("You currently do not have accesss to app", "warning")
        return redirect(url_for("main.home"))
    league = current_user.club.get_league_by_id(id)
    if league is None:
        return redirect(url_for("main.home"))
    if request.method == "POST":
        try:
            data = request.json
            if data['msg'] == 'save':
                apply_edits(league, json.loads(data['data']))
                db.session.commit()
                # flash("League updated successfully.", "success")
                return jsonify({"status": "success"})
            if data["msg"] == "schedule-all":
                league.delete_all_game_events()
                db.session.commit()
                print("Schedule All")
                for flight in league.flights:
                    s = Scheduler(league, Scheduler.SINGLE_FLIGHT, flight_id=flight.id)
                    stats = s.run()
                    current_user.club.update_statistics(stats)
                    db.session.commit()
                for flight in league.flights: #runs better the second time after some prepopulation :-/
                    s = Scheduler(league, Scheduler.SINGLE_FLIGHT, flight_id=flight.id)
                    stats = s.run()
                    current_user.club.update_statistics(stats)
                    db.session.commit()
                return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "failure", "error": str(e)})

    return render_template(
        "league/edit.html",
        simple_form=SimpleForm(),
        league=league,
        club=current_user.club,
    )


@blueprint.route("/schedule/<int:id>", methods=["GET", "POST"])
@login_required
def schedule_league(id):
    """
    This function handles requests to schedule a league and updates the league's
    schedules accordingly.

    Args:
        id (int): The `id` input parameter is passed as an argument to the
            `get_league_by_id` method of the current user's club object.

    Returns:
        dict: The output returned by this function is a JSON object with the
        following structure:
        
        {
        "status": "success",
        "data": [
        {
        "id": flight.id,
        "report": flight.report
        } for flight в league.flights
        ]
        }
        
        This means that the function successfully scheduled games and generated a
        report for the specified league.

    """
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        flash("You currently do not have accesss to app", "warning")
        return redirect(url_for("main.home"))
    league = current_user.club.get_league_by_id(id)
    if league is None:
        return redirect(url_for("main.home"))
    if request.method == "POST":
        try:
            data = request.json
            if data["contents"] == "games":
                create_games_from_request(league, data["data"])
                # league.clean()
                db.session.commit()
                s = Scheduler(league, Scheduler.GENERATE_REPORT)
                s.report()
                db.session.commit()
                return jsonify(
                    {
                        "status": "success",
                        "data": [
                            {"id": flight.id, "report": flight.report}
                            for flight in league.flights
                        ],
                    }
                )
            elif data["contents"] == "schedule":
                s = Scheduler(
                    league, Scheduler.SINGLE_FLIGHT, flight_id=data["data"]["flight_id"]
                )
                stats = s.run()
                current_user.club.update_statistics(stats)
                db.session.commit()
                return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "failure", "error": str(e)})
    return render_template(
        "league/schedule.html",
        simple_form=SimpleForm(),
        league=league,
        club=current_user.club,
    )


@blueprint.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_league(id):
    """
    This function deletes a league with the given ID from the database and redirects
    the user to the home page if the deletion was successful.

    Args:
        id (int): The `id` input parameter passes the league ID as a foreign key
            value to be deleted from the database.

    Returns:
        : Based on the code provided above and assuming current_user is not None
        and current_user.primary_membership_id is not None (i.e., the user is
        authenticated and has a primary membership), the output returned by this
        function is:

        A 302 redirect to the home page.

    """
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        flash("You currently do not have accesss to app", "warning")
        return redirect(url_for("main.home"))
    league = current_user.club.get_league_by_id(id)
    if league is not None:
        db.session.delete(league)
        db.session.commit()
    return redirect(url_for("main.home"))


@blueprint.route("/new", methods=["GET", "POST"])
@login_required
def create_league():
    """
    This function handles a POST request to create a league and performs the
    following actions:
    1/ It reads a CSV file containing league data and converts it to a Python
    dictionary using the `league_wizard_csv_to_dicts` function.
    2/ It checks if the received POST data is valid JSON format.
    3/ It processes the received data and performs further actions.
    4/ It returns a JSON response with the status of the operation (success or
    failure) and any relevant error message.

    Returns:
        dict: Based on the code provided:

        The output returned by this function is `jsonify({"status": "success"}`)
        if the input data is valid and `jsonify({"status": "failure", "error":
        str(e)})` if there is an exception.

    """
    my_club = current_user.club
    player_names = [player.full_name for player in my_club.players]
    players_json = json.dumps(player_names)

    if request.method == "POST":
        try:
            data = request.json
            if "cleaned" in data:
                print("Data contains the field 'cleaned'.")

                league = build_league_from_json(my_club, data)
                league.log()
                db.session.commit()
                return jsonify(
                    {
                        "status": "success",
                        "redirect_url": url_for("league.edit_league", id=league.id),
                    }
                )
            else:
                print("Data does not contain the field 'cleaned'.")
                league_dict = league_wizard_csv_to_dicts(data)
                return jsonify({"status": "success", "data": league_dict})
        except Exception as e:
            return jsonify({"status": "failure", "error": str(e)})
    return render_template(
        "league/create.html",
        club=my_club,
        players_json=players_json,
        simple_form=SimpleForm(),
    )
