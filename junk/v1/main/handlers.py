from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    session,
)
from werkzeug.urls import url_parse
from app import db
from app.main import bp
from app.models.user import User 
from app.models.club import Club
from app.forms import (
    LoginForm,
    ProfileUpdateForm,
    RegistrationForm,
    AddCourtForm,
    EditCourtForm,
    AddFlightForm,
    EditFlightForm,
    EditClubAdminForm,
    AddPlayerForm,
    EditPlayerForm,
)
from flask_login import current_user, login_user, logout_user, login_required
from app.utils import *
from app.CSVtools import *

@bp.before_request
def before_request():
    session.pop("_flashes", None)

@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
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
        "index.html",
        title="Home",
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

@bp.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="404"), 404

@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileUpdateForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.commit()
        flash("Password updated!")
    return render_template("page-user-profile.html", title="Profile", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("main.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        clubname = form.club.data
        club = Club.query.filter(Club.name.ilike(clubname)).first()
        if club is None:
            club = Club(name=clubname)
            db.session.add(club)
            user.club_authenticated = 1
        user.set_club(club)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("main.login"))
    return render_template("register.html", title="Register", form=form)
