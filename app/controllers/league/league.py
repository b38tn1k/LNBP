from flask import Blueprint, render_template, abort, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.forms import SimpleForm
from app.forms.club_forms import ClubSetup, FacilitySetup
from app.models import db
from app.models.clubs import Club, Facility
from app.services.league_services import league_wizard_csv_to_dicts
import json

blueprint = Blueprint('league', __name__)

@blueprint.before_request
def check_for_membership(*args, **kwargs):
    # Ensure that anyone that attempts to pull up the dashboard is currently an active member
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        flash('You currently do not have accesss to app', 'warning')
        return redirect(url_for("main.home"))
    
@blueprint.route('/new', methods=["GET", "POST"])
@login_required
def create_league():
    if request.method == 'POST':
        with open('csv_league_import_example.json', 'r') as f:
            data = json.load(f)
            league_wizard_csv_to_dicts(data)
        try:
            print(request)
            data = request.json
            print("Received data: ", data)
            # with open('received_data.json', 'w') as f:
            #     json.dump(data, f)
            # Further processing
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "failure", "error": str(e)})
    return render_template('league/create.html', club=current_user.club, simple_form=SimpleForm())