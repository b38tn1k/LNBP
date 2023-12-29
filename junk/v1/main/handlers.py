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
    """
    The given function `before_request` clears the "_flashes" session variable
    using the `pop()` method and sets its return value to `None`.

    """
    session.pop("_flashes", None)

@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    # club = Club.query.filter_by(name=clubname).first_or_404()
    """
    This function renders an HTML template "index.html" and returns it with some
    dynamic data:
    1/ It gets the current user's club using `current_user.club`.
    2/ It initializes and filters forms for adding/editing courts and flights.
    3/ If a form is validated and submitted (using `validate_on_submit()`), it
    performs respective actions (adds a court or flight) and resets the form's data.
    4/ It provides dynamic forms for adding a player and editing a player.
    5/ It returns a rendering of "index.html" with all these data and forms.

    Returns:
        : Based on the code provided above and neglecting any external libraries
        or frameworks being used within it:
        
        The output returned from `index()` should be an HTML page rendered using
        render_template() function template named 'index.html'.

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
    """
    This function takes an `error` parameter and returns a HTTP 404 response with
    the rendering of a template named "404.html".

    Args:
        error (): The `error` input parameter is passed as an optional argument
            to the `page_not_found()` function and is not used anywhere within the
            function body.

    Returns:
        str: The output returned by this function is a 404 HTTP response with the
        rendered template "404.html" and a title of "404".

    """
    return render_template("404.html", title="404"), 404

@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    This function defines a Flask view function named `profile` that updates the
    password for the current user. When the user submits the form with valid data
    (password and confirm password), the function sets the user's password using
    the `set_password()` method and commits any changes to the database.

    Returns:
        : The output returned by the function is a rendering of the template
        "page-user-profile.html" with the title "Profile" and the form object "form".

    """
    form = ProfileUpdateForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.commit()
        flash("Password updated!")
    return render_template("page-user-profile.html", title="Profile", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    This function implements a login system for the web application.

    Returns:
        : The output returned by the `login()` function is a redirect to the next
        page specified by the `next` parameter or the URL for the `main.index`
        view if no `next` parameter is provided.

    """
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
    """
    The given function `logout()` logs out the current user and redirects them to
    the main index page (`main.index`) after completing the logout process.

    Returns:
        : The output returned by the `logout` function is `redirect(url_for("main.index"))`,
        which is a URL for the "index" view of the "main" module.

    """
    logout_user()
    return redirect(url_for("main.index"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    This function is the `register()` view function for a Flask web application.
    It handles the registration of new users and redirects them to the login page
    after successfully registering. Here's what it does:
    1/ If the user is already authenticated (logged-in), it redirects them to the
    main index page.
    2/ Else (i.e., if the user is not authenticated), it creates a new `RegistrationForm`
    and binds it to the `form` variable.
    3/ If the form is valid (i.e., all fields are filled out and there are no
    errors), it creates a new `User` instance with the provided data (username:username
    field; email:email field; password:password field).
    4/ It also sets the `club_authenticated` flag to 1 if the user has selected a
    club during registration.

    Returns:
        : The output returned by this function is a redirect to the `main.login`
        view with a flash message "Congratulations..".

    """
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
