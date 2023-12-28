from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db

blueprint = Blueprint('player', __name__)

@blueprint.route('/<hashid:player_id>', methods=["GET", "POST"])
@login_required
def index(player_id):
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        flash('You currently do not have accesss to app', 'warning')
        return redirect(url_for("main.home"))
    club = current_user.club
    player = next((p for p in club.players if p.id == player_id), None)
    return render_template('player/player.html', club=club, player=player)


@blueprint.route('/delete/<int:player_id>', methods=["POST"])
@login_required
def delete_player(player_id):
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