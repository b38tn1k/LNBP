from flask import (
    render_template,
    redirect,
    url_for,
    request,
)
from app import db
from app.courts import bp

from app.models.court import Court

from app.forms import (
    AddCourtForm,
    EditCourtForm,
)
from flask_login import current_user, login_required
from app.utils import *
from app.CSVtools import *


@bp.route("/courts/<int:court_id>/delete", methods=["POST"])
@login_required
def delete_court(court_id):
    """
    This function deletes a Court object with the given court ID and redirects the
    user to either the list of courts page or the main index page depending on the
    previous page visited.

    Args:
        court_id (int): The `court_id` input parameter identifies the specific
            court record to be deleted from the database.

    Returns:
        int: Based on the code provided:
        
        The output returned by `delete_court` function is a redirect to either
        `courts.courts` or `main.index` depending on the `request.referrer` variable.

    """
    court = Court.query.get_or_404(court_id)
    db.session.delete(court)
    db.session.commit()
    if "courts" in request.referrer:
        return redirect(url_for("courts.courts"))
    else:
        return redirect(url_for("main.index"))


@bp.route("/courts/<int:court_id>/edit", methods=["GET", "POST"])
@login_required
def edit_court(court_id):
    """
    This function takes a `court_id` parameter and renders a template page for a
    specific court based on the data retrieved from the database.

    Args:
        court_id (int): The `court_id` input parameter passes a unique identifier
            to the function that specifies which Court object to retrieve from the
            database.

    Returns:
        str: The output returned by the `edit_court()` function is a rendered HTML
        template named "page-court.html" with the following data:
        
        	- `title`: The court name
        	- `calendar_data`: The timeslots JSON data of the court

    """
    club = current_user.club
    court = Court.query.get_or_404(court_id)
    return render_template(
        "page-court.html",
        title=court.court_name,
        calendar_data=court.get_timeslots_json(),
    )


@bp.route("/courts", methods=["GET", "POST"])
@login_required
def courts():
    """
    This function renders a HTML page with a form to either add or edit a court
    for the current user's club.

    Returns:
        tuple: The output returned by this function is a dictionary with the
        following keys:
        
        	- club: The current user's club object
        	- add_court_form: An instance of AddCourtForm
        	- edit_court_form: An instance of EditCourtForm
        	- title: The name of the club

    """
    club = current_user.club
    acf = AddCourtForm()
    ecf = EditCourtForm()
    if acf.validate_on_submit():
        club.add_court(acf.court_name.data)
        acf.court_name.data = ""
        db.session.commit()
    return render_template(
        "page-courts.html", club=club, add_court_form=acf, edit_court_form=ecf, title=club.name
    )
