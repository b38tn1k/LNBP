from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db
from app.forms.player_form import PlayerForm
from app.forms import SimpleForm

blueprint = Blueprint('player', __name__)

@blueprint.route('/<hashid:player_id>', methods=["GET", "POST"])
@login_required
def index(player_id):
    """
    The function `index(player_id)`:
    1/ Checks if the current user is authenticated and has a primary membership;
    if not it redirects to the home page.
    2/ Retrieves the club related to the current user's membership.
    3/ Fetches the player with the specified `player_id` from the current user's
    club.
    4/ Renders the `player.html` template with the `club` and `player` objects.

    Args:
        player_id (int): The `player_id` input parameter specifies the ID of the
            player to be retrieved and rendered on the HTML page.

    Returns:
        : The output returned by the function is a renderered template
        ('player/player.html') with the data club and player.

    """
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        flash('You currently do not have accesss to app', 'warning')
        return redirect(url_for("main.home"))
    club = current_user.club
    player = next((p for p in club.players if p.id == player_id), None)
    form = PlayerForm(obj=player)
    if form.validate_on_submit():
        form.populate_obj(player)
        db.session.commit()
        flash('Player information updated successfully.', 'success')

    return render_template('player/player.html', club=club, my_player=player, form=form, simple_form=SimpleForm())


@blueprint.route('/delete/<int:player_id>', methods=["POST"])
@login_required
def delete_player(player_id):
    """
    This function takes a player ID as input and checks if the player belongs to
    the current user's club. If the player exists and is owned by the current
    user's club., it deletes the player from the database and returns a success
    response with a message indicating that the player has been deleted.

    Args:
        player_id (int): The `player_id` input parameter identifies the player to
            be deleted from the current user's club.

    Returns:
        dict: Based on the code provided:
        
        Output: JSON response with status "success" and message "Player deleted"
        (200 HTTP status code).

    """
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401

    # Check if the player belongs to the current user's club
    club = current_user.club
    player = next((p for p in club.players if p.id == player_id), None)

    if player:
        # Perform deletion logic
        db.session.delete(player)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Player deleted'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Player not found'}), 404
    

@blueprint.route('/new', methods=["GET", "POST"])
@login_required
def new_player():
    """
    This function creates a new player for a club based on user input. It first
    checks if the user is authenticated and has a primary membership id before
    redirecting to the home page if they don't. If the user is authenticated and
    has a primary membership id it then creates a new PlayerForm with default
    values populated from the current user's club and then renders the 'player/new.html'
    template with that form prepopulated with values.

    Returns:
        : The output returned by this function is a HTML page with the rendering
        of template 'player/new.html' and an alert message "Player information
        updated successfully." if the form is validated.

    """
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        flash('You currently do not have accesss to app', 'warning')
        return redirect(url_for("main.home"))
    club = current_user.club    
    form = PlayerForm()
    if form.validate_on_submit():
        player = club.new_player("", "")
        form.obj = player
        form.populate_obj(player)
        db.session.commit()
        flash('Player information updated successfully.', 'success')

    return render_template('player/new.html', club=club, form=form, simple_form=SimpleForm())
