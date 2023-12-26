from flask import Blueprint, render_template, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.club_services import get_club_facility_summary, get_leagues_by_status

from app.models.teams import Team

blueprint = Blueprint('dashboard_home', __name__)

@blueprint.route('/')
@login_required
def index():
    if current_user.active_memberships:
        return redirect(url_for('.home', team_id=current_user.active_memberships[0].team.id))
    else:
        flash("You are not part of any teams", 'warning')
        return redirect(url_for('user_settings.memberships'))

@blueprint.route('/<hashid:team_id>')
@login_required
def home(team_id):
    team = Team.query.get(team_id)
    if not team or not team.has_member(current_user):
        abort(404)

    
    facility_summary = get_club_facility_summary(current_user.club.id)
    leagues_summary = get_leagues_by_status(current_user.club.id)
    print(leagues_summary)

    return render_template('dashboard/home.html', facility_summary=facility_summary, leagues=leagues_summary, team=team, club=current_user.club)
    # return render_template('dashboard/home_backup.html', club=current_user.club, team=team)
