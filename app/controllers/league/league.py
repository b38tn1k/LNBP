from flask import Blueprint, render_template, abort, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms import SimpleForm
from app.forms.club_forms import ClubSetup, FacilitySetup
from app.models import db
from app.models.clubs import Club, Facility

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
    return render_template('league/create.html', club=current_user.club)
    