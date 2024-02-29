from collections import Counter
from datetime import datetime
from app.models.clubs import Facility, Club, League, LeaguePlayerAssociation, Timeslot
from app import db

def get_club_facility_summary(club_id):
    # Fetch all facilities that belong to the club
    facilities = Facility.query.filter_by(club_id=club_id).all()

    # If there are no facilities, return None
    if not facilities:
        return None

    # Count the total number of facilities
    total_count = len(facilities)

    # Count facilities grouped by asset_type
    asset_types = [facility.asset_type for facility in facilities]
    asset_type_count = Counter(asset_types)

    # Construct the summary dictionary
    summary = {
        'total_count': total_count,
        'asset_type': dict(asset_type_count),
    }

    return summary

def get_leagues_by_status(club_id, past_league_limit=10):
    # Fetch all leagues belonging to a club
    leagues = League.query.filter_by(club_id=club_id).all()
    if not leagues:
        return None
    current_date = datetime.utcnow()
    
    # Initialize containers for categorized leagues
    current_leagues = []
    planned_leagues = []
    past_leagues = []

    # Iterate over each league to categorize and collect details
    for league in leagues:
        # Find the league's start date
        start_date = league.start_date

        # Determine the end date based on the timeslots
        timeslots = Timeslot.query.filter_by(league_id=league.id).all()
        if timeslots:
            end_date = max(ts.end_time for ts in timeslots)
        else:
            end_date = start_date

        # Calculate the player count through the League-Player associations
        player_count = db.session.query(LeaguePlayerAssociation).filter_by(league_id=league.id).count()
        if league:
            issue_count = league.get_total_flight_issues()
        else:
            issue_count = 0

        # Prepare league summary
        league_summary = {
            'name': league.name,
            'start_date': start_date.strftime('%m/%d/%y'),
            'end_date': end_date.strftime('%m/%d/%y'),
            'player_count': player_count,
            'id' : league.id,
            'issue_count' : issue_count
        }

        # Categorize the league
        if start_date > current_date:
            planned_leagues.append(league_summary)
        elif end_date < current_date:
            past_leagues.append(league_summary)
        else:
            current_leagues.append(league_summary)

    # Sort and limit the number of past leagues
    past_leagues = sorted(past_leagues, key=lambda x: x['end_date'], reverse=True)[:past_league_limit]

    return {
        'current': current_leagues,
        'planned': planned_leagues,
        'past': past_leagues
    }
