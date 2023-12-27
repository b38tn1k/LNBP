from flask import Blueprint, render_template, abort, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.forms import SimpleForm
from app.forms.club_forms import ClubSetup, FacilitySetup
from app.models import db
from app.models.clubs import Club, Facility
from app.services.league_services import league_wizard_csv_to_dicts, build_league_from_json
import json

blueprint = Blueprint('league', __name__)

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
        flash('You currently do not have accesss to app', 'warning')
        return redirect(url_for("main.home"))

@blueprint.route('/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit_league(id):
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        flash('You currently do not have accesss to app', 'warning')
        return redirect(url_for("main.home"))
    league = current_user.club.get_league_by_id(id)
    if league is None:
        return redirect(url_for("main.home"))
    return render_template('league/edit.html', league=league)

@blueprint.route('/delete/<int:id>', methods=["GET", "POST"])
@login_required
def delete_league(id):
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        flash('You currently do not have accesss to app', 'warning')
        return redirect(url_for("main.home"))
    league = current_user.club.get_league_by_id(id)
    if league is not None:
        db.session.delete(league)
        db.session.commit()
    return redirect(url_for("main.home"))


@blueprint.route('/new', methods=["GET", "POST"])
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
    if request.method == 'POST':
        try:
            data = request.json
            if 'cleaned' in data:
                print("Data contains the field 'cleaned'.")
                my_club = current_user.club
                build_league_from_json(my_club, data)
                db.session.commit()
                return jsonify({"status": "success"})
            else:
                print("Data does not contain the field 'cleaned'.")
                league_dict = league_wizard_csv_to_dicts(data)
                return jsonify({"status": "success", "data": league_dict})
        except Exception as e:
            return jsonify({"status": "failure", "error": str(e)})
    return render_template('league/create.html', club=current_user.club, simple_form=SimpleForm())