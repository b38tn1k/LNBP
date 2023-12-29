from flask import (
    render_template,
    redirect,
    url_for,
)
from app import db
from app.club import bp
from app.models.user import User 
from app.models.club import Club

from app.forms import (
    AddCourtForm,
    EditCourtForm,
    AddFlightForm,
    EditFlightForm,
    EditClubAdminForm,
    AddPlayerForm,
    EditPlayerForm,
)
from flask_login import current_user, login_required
from app.utils import *
from app.CSVtools import *

@bp.route("/club/<clubname>/admin_gate")
@login_required
def admin_gate(clubname):
    club = Club.query.filter_by(name=clubname).first_or_404()
    return render_template("no_auth.html", club=club, title=club.name)

@bp.route("/club/<clubname>", methods=["GET", "POST"])
@login_required
def club(clubname):
    # club = Club.query.filter_by(name=clubname).first_or_404()
    club = current_user.club
    acf = AddCourtForm()
    ecf = EditCourtForm()
    alf = AddFlightForm()
    elf = EditFlightForm()
    ecaf = EditClubAdminForm()
    fileform = createFileForm(club)

    if acf.validate_on_submit():
        club.add_court(acf.court_name.data)
        acf.court_name.data = ""
        db.session.commit()
    if alf.validate_on_submit():
        # club.add_flight(alf.flight_name.data)
        alf.flight_name.data = ""
        # db.session.commit()
    apf = AddPlayerForm()
    epf = EditPlayerForm()
    if apf.validate_on_submit():
        club.add_player(apf.player_name.data, apf.player_email.data)
        apf.player_name.data = ""
        apf.player_email.data = ""
        db.session.commit()
    return render_template(
        "page-club.html",
        title=clubname,
        club=club,
        add_court_form=acf,
        edit_court_form=ecf,
        add_flight_form=alf,
        edit_flight_form=elf,
        club_admin_form=ecaf,
        add_player_form=apf,
        edit_player_form=epf,
        fileform = fileform,
    )

@bp.route("/users/<int:user_id>/toggle_auth", methods=["POST"])
@login_required
def toggle_user_auth(user_id):
    user = User.query.get(user_id)
    club = user.club
    user.toggle_auth()
    current_user.club_authenticated = 1  # users cant deauth themselves
    db.session.commit()
    return redirect(url_for("club.club", clubname=club.name))

