from collections import Counter
from datetime import datetime
from app.models.clubs import Facility, Club, League, LeaguePlayerAssociation, Timeslot
from app import db

def get_club_facility_summary(club_id):
    # Fetch all facilities that belong to the club
    """
    This function gets a club's facilities and returns a dictionary with two items:
    'total_count' (the number of facilities) and 'asset_type' (a dict counting the
    facilities by asset type).

    Args:
        club_id (int): The `club_id` input parameter is used to filter the facilities
            that belong to a specific club.

    Returns:
        dict: The output returned by the function `get_club_facility_summary()`
        is a dictionary with two key-value pairs:
        
        	- 'total_count': an integer representing the total number of facilities
        belonging to the specified club.
        	- 'asset_type': a dictionary mapping asset types to their counts.

    """
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
    """
    This function retrieves all leagues associated with a given club ID and
    categorizes them based on their start date into current leagues (active),
    planned leagues (upcoming), and past leagues (finished).

    Args:
        club_id (int): The `club_id` input parameter specifies which clubs' leagues
            should be retrieved.
        past_league_limit (int): The `past_league_limit` input parameter limits
            the number of past leagues returned by the function.

    Returns:
        dict: The output returned by the function `get_leagues_by_status` is a
        dictionary with three key-value pairs:
        
        	- `current`: A list of dictionaries containing details about current leagues.
        	- `planned`: A list of dictionaries containing details about planned
        leagues that have not yet started.
        	- `past`: A list of dictionaries containing details about past leagues
        that have already ended.

    """
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

        issue_count = league.get_total_flight_issues()

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
