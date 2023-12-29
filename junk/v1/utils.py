from flask_login import current_user
from flask import render_template

def checkClub(club, user):
    return club.has_user(user) and user.club_authenticated == 1


def checkFlight(flight):
    return current_user.club.has_flight(flight)


def checkCourt(court):
    return current_user.club.has_court(court)


def not_admin(club):
    return render_template("no_auth.html", club=club)

