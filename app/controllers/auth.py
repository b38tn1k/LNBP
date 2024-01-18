from flask import Blueprint, render_template, flash, request, redirect, url_for, session, abort
from flask_login import login_user, logout_user, login_required, current_user

import app.constants as constants

from app.forms import SimpleForm
from app.forms.login import LoginForm, SignupForm, RequestPasswordResetForm, ChangePasswordForm
from app.models import db
from app.models.user import User
from app.models.teams import TeamMember
from app.mailers.auth import ConfirmEmail, ResetPassword
from app.extensions import login_manager, token, limiter

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(userid):
    """
    This function loads a user object based on a given `userid` using SQLAlchemy's
    `Query` class.

    Args:
        userid (int): The `userid` input parameter is used to retrieve a specific
            user object from the database based on its ID.

    Returns:
        : The output returned by this function is `None`, as there is no user with
        the given ID `userid` on the table `User`.

    """
    return User.query.get(userid)

@login_manager.unauthorized_handler
def unauthorized():
    """
    This function called `unauthorized` sets the value of a session variable
    `after_login` to the current URL requested before redirecting the user to the
    login page with the provided `login_hint`.

    Returns:
        : The output returned by `unauthorized()` is a HTTP Redirect to the
        `auth.login` route with the `login_hint` parameter set to the value of `request.args.get('login_hint')`.

    """
    session['after_login'] = request.url
    login_hint = request.args.get('login_hint')
    return redirect(url_for('auth.login', login_hint=login_hint))

@auth.route("/login", methods=["GET", "POST"])
@limiter.limit("20/minute")
def login():
    """
    This function implements a login functionality for the application using
    Flask-WTF and flask_oauthlibit.

    Returns:
        : The output returned by this function is a rendering of the "auth/login.html"
        template with the "form" object and a "success" message flash.

    """
    if not constants.ALLOW_PASSWORD_LOGIN:
        return render_template("auth/oauth_only_login.html")

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()
        session['current_team_membership_id'] = user.primary_membership_id
        login_user(user)
        # flash("Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for("main.home"))

    return render_template("auth/login.html", form=form)

@auth.route("/signup", methods=["GET", "POST"])
@limiter.limit("10/minute")
def signup():
    """
    This function handles user signups for a LeagueNinja application. It checks
    if signups are allowed and validates the submitted form data. If the form is
    validated successfully (i.e., the email address and password provided are
    correct), it creates a new user account and sends a confirmation email (if required).

    Returns:
        : Based on the code provided:
        
        The output returned by this function is a HTTP redirection to either the
        "dashboard_home.index" URL if `constants.REQUIRE_EMAIL_CONFIRMATION` is
        false or the confirmation email sent via `ConfirmEmail(user)` if it is true.

    """
    if not constants.ALLOW_SIGNUPS:
        return abort(404)

    form = SignupForm(invite_secret=request.args.get('invite_secret'))

    if form.validate_on_submit():
        team_secret = form.invite_secret.data
        invite = (TeamMember.query.filter_by(invite_secret=team_secret, activated=False)
                            .one_or_none())

        if invite:
            user = User(form.email.data, form.password.data,
                        email_confirmed=True, team=invite.team)
            invite.user = user
            db.session.add(invite)
        else:
            user = User(form.email.data, form.password.data, team_name=form.club.data)
        db.session.add(user)
        db.session.commit()
        session['current_team_membership_id'] = user.primary_membership_id
        login_user(user)

        if constants.REQUIRE_EMAIL_CONFIRMATION:
            # Send confirm email
            ConfirmEmail(user).send()

        flash("Welcome to LeagueNinja.", "success")
        return redirect(request.args.get("next") or url_for("dashboard_home.index"))

    return render_template("auth/signup.html", form=form, invite_secret=request.args.get('invite_secret'))

@auth.route("/auth/logout")
def logout():
    """
    This function logs out the user and clears the session data before redirecting
    them to the home page.

    Returns:
        : The output returned by the `logout` function is a redirect to the `/home`
        route.

    """
    logout_user()
    session.clear()
    return redirect(url_for("main.home"))

@auth.route("/confirm/<string:code>")
def confirm(code):
    """
    This function confirms an email address for a user.

    Args:
        code (str): The `code` input parameter is a confirmation code that is sent
            to the user's email address as part of the email verification process.

    Returns:
        None: The output returned by this function depends on the input value of
        `code`.

    """
    if not constants.REQUIRE_EMAIL_CONFIRMATION:
        abort(404)

    try:
        email = token.decode(code, salt=constants.EMAIL_CONFIRMATION_SALT)
    except Exception:
        email = None

    if not email:
        # TODO: Render a nice error page here.
        return abort(404)

    user = User.query.filter_by(email=email).first()
    if not user:
        return abort(404)
    user.email_confirmed = True
    db.session.commit()

    if current_user == user:
        flash('Succesfully confirmed your email', 'success')
        return redirect(url_for("dashboard_home.index"))
    else:
        flash('Confirmed your email. Please login to continue', 'success')
        return redirect(url_for("auth.login"))


@auth.route("/auth/resend-confirmation", methods=["GET", "POST"])
@limiter.limit("5/minute")
@login_required
def resend_confirmation():
    """
    This function allows a user to resend the email confirmation for their account.
    It checks if the user's email is confirmed and if not sends a confirmation email.

    Returns:
        : Based on the code provided and assuming `constants.REQUIRE_EMAIL_CONFIRMATION`
        is set to `True`, if the current user has already confirmed their email
        address (i.e., `current_user.email_confirmed == True`), the function returns
        a redirect to the dashboard home page (`redirect(url_for("dashboard_home.index"))`).
        If not (i.e., `current_user.email_confirmed == False`), it renders the
        template `auth/resend_confirmation.html` and returns the rendered HTML
        with the form populated.

    """
    if not constants.REQUIRE_EMAIL_CONFIRMATION:
        abort(404)
    if current_user.email_confirmed:
        return redirect(url_for("dashboard_home.index"))

    form = SimpleForm()
    if form.validate_on_submit():
        if ConfirmEmail(current_user).send():
            flash(
                "Sent confirmation to {}".format(
                    current_user.email),
                'success')
        return redirect(url_for("dashboard_home.index"))

    return render_template('auth/resend_confirmation.html', form=form)

@auth.route("/auth/reset_password", methods=["GET", "POST"])
@limiter.limit("20/hour")
def request_password_reset():
    """
    This function allows a user to request a password reset by entering their email
    address and sends a password reset email if the email is registered and
    associated with a user account.

    Returns:
        None: The output returned by this function is a rendering of the template
        "auth/request_password_reset.html" with the variable "form" set to an
        instance of "RequestPasswordResetForm".

    """
    if not current_user.is_anonymous:
        flash('You must be logged out to reset your password', 'warning')
        return redirect(url_for("dashboard_home.index"))
    form = RequestPasswordResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()
        if user:
            ResetPassword(user).send()
            flash("We sent you a password reset email.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Hmm. That email doesn't appear to be registered ", "success")
    return render_template("auth/request_password_reset.html", form=form)

@auth.route("/auth/reset_password/<string:code>", methods=["GET", "POST"])
@limiter.limit("20/hour")
def reset_password(code):
    """
    This function allows a user to reset their password by entering a reset code
    sent to their email.

    Args:
        code (str): The `code` input parameter is a token sent to the user via
            email to verify their identity for password reset.

    Returns:
        : The output returned by this function is a HTTP redirect to the dashboard
        home page with a "success" flash message.

    """
    if not current_user.is_anonymous:
        flash('You must be logged out to reset your password', 'warning')
        return redirect(url_for("dashboard_home.index"))

    try:
        email = token.decode(code, salt=constants.PASSWORD_RESET_SALT)
    except Exception:
        email = None

    if not email:
        return abort(403)

    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).one()
        user.password = form.password.data
        db.session.commit()
        login_user(user)

        flash("Changed your password succesfully", "success")
        return redirect(request.args.get("next") or url_for("dashboard_home.index"))

    return render_template("auth/reset_password.html", form=form)


@auth.route("/reauth", methods=["GET", "POST"])
def reauth():
    """
    This function called `reauth` displays a login form to re-authenticate the
    user using `LoginForm()` if it was sent as a post request after validation
    using `validate_on_submit`. If the form data passes the validate test the
    function logs the user back into the app by querying for them by email on the
    user model with filter_by and passing that as login_user then returns the
    response from login_user along with flash(which is a success message). It
    finishes off by either redirecting to a page requested after next or using
    url_for() method if nothing was specified to go to the settings page.

    Returns:
        : The output returned by this function is a rendered template "reauth.html"
        with a Form object "form".

    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()
        login_user(user)

        flash("Re-authenticated successfully.", "success")
        return redirect(request.args.get("next", url_for("user_settings.index")))
    return render_template("reauth.html", form=form)

@auth.route('/invite/<hashid:invite_id>/join')
@login_required
def join_team(invite_id):
    """
    This function joins a user to a team based on an invite ID. If the invite is
    not found or the user and invite are not for the same person then it returns
    an error with a 404 code.

    Args:
        invite_id (str): The `invite_id` parameter is used to identify the specific
            team invitation that the user is joining.

    Returns:
        : The output returned by this function is a HTTP redirection to the URL
        for the dashboard home page (`redirect(url_for("dashboard_home.index"))`).

    """
    invite = TeamMember.query.get(invite_id)
    if not invite or invite.user != current_user:
        return abort(404)

    invite.activate(current_user.id)
    return redirect(url_for("dashboard_home.index"))

@auth.route('/join/<hashid:invite_id>/<string:secret>')
@limiter.limit("20/minute")
def invite_page(invite_id, secret):
    """
    This function handles the login process for an invited user using a secret key.

    Args:
        invite_id (int): The `invite_id` input parameter specifies the ID of the
            invitation to be viewed and verified.
        secret (str): The `secret` input parameter verifies that the submitted
            secret code matches the one that was originally sent to the user.

    Returns:
        : The output returned by this function is a rendered HTML page with the
        template "auth/invite.html" and the provided form data.

    """
    invite = TeamMember.query.get(invite_id)
    if not invite.invite_secret or invite.invite_secret != secret or invite.activated:
        return abort(404)

    if current_user.is_authenticated and invite.user == current_user:
        return redirect(url_for(".join_team", invite_id=invite.id))

    form = SignupForm(invite_secret=invite.invite_secret)
    return render_template("auth/invite.html", form=form, invite=invite)

