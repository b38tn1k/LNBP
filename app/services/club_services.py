from collections import Counter
from datetime import datetime
from app.models.clubs import Facility, Club, League, LeaguePlayerAssociation, Timeslot
from app import db

def get_club_facility_summary(club_id):
    # Fetch all facilities that belong to the club
    """
    This function fetches a list of all facilities associated with a particular
    club, and then summarizes the information by counting the total number of
    facilities and grouping them by asset type. The resulting summary dictionary
    contains two keys: `total_count` (the total number of facilities), and
    `asset_type` (a dictionary containing the count of each asset type).

    Args:
        club_id (str): The `club_id` input parameter is used to filter the Facility
            model to retrieve only the facilities that belong to the specified
            club. Without this parameter, the function would return all facilities
            from the database, not just those associated with the given club.

    Returns:
        dict: The function `get_club_facility_summary` returns a dictionary
        summarizing the facilities belonging to a specific club. The dictionary
        contains two keys:
        
        1/ 'total_count': the total number of facilities belonging to the club.
        2/ 'asset_type': a count of the different asset types (e.g., courts, fields,
        etc.) of the facilities.

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
    This function performs the following actions:
    1/ It retrieves all leagues belonging to a specific club using the
    `League.query.filter_by(club_id=club_id).all()` method.
    2/ It initializes separate containers for categorized leagues (current, planned,
    and past) to store league summaries.
    3/ It iterates over each league in the list of leagues and calculates the
    player count and total flight issues using associations with `LeaguePlayerAssociation`
    and `league.get_total_flight_issues()` methods, respectively.
    4/ It prepares a league summary for each league by combining the calculated
    player count, start date, end date, and issue count into a dictionary.
    5/ It categorizes each league based on its start date by storing planned leagues
    in a list, past leagues in another list, and current leagues in yet another list.
    6/ Finally, it returns an object containing the `current`, `planned`, and
    `past` lists of leagues, sorted by end date (or start date for planned leagues).

    Args:
        club_id (int): The `club_id` input parameter in the `get_leagues_by_status`
            function serves as a filter to fetch only leagues that belong to the
            specified club. It is used in the `League.query.filter_by(club_id=club_id).all()`
            line of the code, where it is passed as an argument to the `filter_by`
            method. By filtering the leagues based on the value of `club_id`, the
            function can return a list of only the leagues that belong to the
            specified club, regardless of their start or end dates.
        past_league_limit (int): The `past_league_limit` input parameter limits
            the number of past leagues returned in the function output. It specifies
            the number of past leagues to be included in the function return, which
            is sorted and limited to the specified value.

    Returns:
        dict: The function returns a dictionary with three keys: `current`,
        `planned`, and `past`. Each key contains a list of league summaries
        categorized based on their start or end dates. The `current` list contains
        leagues that are currently ongoing, the `planned` list contains leagues
        that will take place in the future, and the `past` list contains leagues
        that have already taken place.

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
