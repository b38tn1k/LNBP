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
