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
    """
    This function filters the `Club` database table using the provided `clubname`,
    and then renders an HTML template called "no_auth.html" with the club object
    as its context.

    Args:
        clubname (str): The `clubname` input parameter is used to retrieve a
            specific Club object from the database using its name.

    Returns:
        dict: The output returned by this function is a rendering of the "no_auth.html"
        template with the `club` and `title` variables set to the filtered club
        object and the club name respectively.

    """
    club = Club.query.filter_by(name=clubname).first_or_404()
    return render_template("no_auth.html", club=club, title=club.name)

@bp.route("/club/<clubname>", methods=["GET", "POST"])
@login_required
def club(clubname):
    # club = Club.query.filter_by(name=clubname).first_or_404()
    """
    This function handles theclub administration pages for the web application.
    It renders a template called "page-club.html" and provides several form objects
    (e.g., AddCourtForm(), EditCourtForm()) that can be used to modify club information.

    Args:
        clubname (str): The `clubname` input parameter is passed as a string and
            is used as the name of the current club that the user is viewing. This
            name is then used to filter the clubs using the `query.filter_by()`
            method to retrieve the first club with the matching name.

    Returns:
        : The output returned by this function is a rendered HTML page with the
        title and club details specified for the given `clubname`, along with
        various forms for adding/editing courts and flights as well as managing
        club administration and players.

    """
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
    """
    This function toggle_user_auth takes a user ID as an input and updates the
    user's authentication status. If the user is authenticated it will de-authenticate
    them otherwise it will authenticate them.

    Args:
        user_id (int): The `user_id` input parameter is used to identify the user
            record to be updated or retrieved from the database.

    Returns:
        : Based on the code provided:
        
        The output returned by this function is `redirect(url_for("club.club", clubname=club.name))`

    """
    user = User.query.get(user_id)
    club = user.club
    user.toggle_auth()
    current_user.club_authenticated = 1  # users cant deauth themselves
    db.session.commit()
    return redirect(url_for("club.club", clubname=club.name))

