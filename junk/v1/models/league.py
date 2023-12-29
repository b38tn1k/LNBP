from app import db
from .player import Player
from .court import Court
from .flight import Flight
from . import Model

def generate_scorecard_from_event(e, fields):
    """
    This function generates a scorecard from an event object "e" and a list of
    fields "fields" by creating two headers and then appending rows for each player
    name found In the event's "player_names" list. The rows are padded with empty
    cells to match the length of the header rows.

    Args:
        e (dict): The `e` input parameter is an event dictionary that contains
            data about a single tennis match.
        fields (list): The `fields` input parameter is a list of additional fields
            to be included under the "Sub's Name" header (after `e['captain_name']`)
            when generating the scorecard from an event.

    Returns:
        str: The output returned by this function is a string concatenation of all
        the player rows with the headers separated by a newline character.

    """
    score_card = []
    header1 = [e['flight_name'], e['readable_time'], e['readable_date']]
    header2 = ["Court", "Name", "Sub's Name"]
    header2.extend(fields)
    score_card.append(header1)
    score_card.append(header2)
    score_card_strings = []
    
    for player in e['player_names']:
        if player == e['captain_name'] :
            player_row = [e['court_name'], player + " (C)", '']
        else:
            player_row = [e['court_name'], player, '']
        h2len = len(header2)
        while len(player_row) != h2len:
            player_row.append("")
        score_card.append(player_row)
    
    for row in score_card:
        mystr = ', '.join(row)
        score_card_strings.append(mystr)
    result = "\n".join(score_card_strings)
    return result


class League(Model):
    id = db.Column(db.Integer, primary_key=True)
    league_name = db.Column(db.String(64), index=True, unique=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id', name='league_admined_club'))
    club = db.relationship('Club', backref='leagues')

    def add_flight(self, flight_name, commit=True):
        """
        This function adds a new Flight object to the database if one with the
        same name and league does not already exist.

        Args:
            flight_name (str): The `flight_name` input parameter is used to identify
                the flight that the method should add or retrieve from the database.
            commit (bool): The `commit` input parameter is used to determine whether
                to immediately commit any changes made to the database after adding
                a new flight.

        Returns:
            : The output returned by this function is `Flight` object if the flight
            with the given name exists already and `None` otherwise.

        """
        check = Flight.query.filter_by(flight_name=flight_name, league=self).first()
        if check is None:
            flight = Flight(flight_name=flight_name, league=self)
            db.session.add(flight)
            if commit:
                db.session.commit()
            return flight
        return check
    
    def delete(self, commit=True):
        """
        This function deletes all flights associated with the object and then
        deletes the object itself from the database.

        Args:
            commit (bool): The `commit` input parameter is a flag that determines
                whether to commit the changes made by the `delete()` function to
                the database immediately after deleting the objects.

        Returns:
            bool: The output returned by this function is `True`.

        """
        for f in self.flights:
            f.on_delete()
            db.session.delete(f)
        db.session.delete(self)
        if commit:
            db.session.commit()
        return True

    def get_events_sorted(self):
        """
        This function takes a list of flights and returns a list of events sorted
        by date and court name.

        Returns:
            dict: The output returned by the `get_events_sorted` function is a
            list of events sorted by date and court name.

        """
        events = []
        for flight in self.flights:
            events.extend(flight.get_events())

        # Sort events by datetime_obj and then by court_name
        sorted_events = sorted(
            events, 
            key=lambda x: (x['datetime_obj'], x['court_name'])
        )
        return sorted_events

    def generate_scorecard_CSV(self):
        """
        This function generates a CSV file with a scorecard for each event (row)
        of a tournament or match.

        Returns:
            str: The function returns a string that consists of newline-separated
            scorecards. Each scorecard is created by concatenating the fields (1st
            Set etc.) and the corresponding values for each event.

        """
        scorecards = []
        fields = ['1st Set', '2nd Set', '3rd Set', 'Games Won', 'Games Lost', 'Sets Won', 'W-L Adjusted']
        events = self.get_events_sorted()
        for e in events:
            scorecards.append(generate_scorecard_from_event(e, fields))
        result = "\n\n".join(scorecards)
        return result
    
    def generate_schedule_CSV(self):
        """
        This function generates a CSV string representing the flight schedule for
        multiple flights by joining together the individual CSV strings generated
        by each flight's `generate_schedule_CSV()` method.

        Returns:
            str: The function "generate_schedule_CSV" returns a string containing
            a list of CSV rows representing the flight schedules for each flight
            object.

        """
        flight_schedules = []
        for flight in self.flights:
            r = flight.generate_schedule_CSV()
            flight_schedules.append(r)
        result = "\n\n".join(flight_schedules)
        return result



'''

League Modes:
1. Flighted League (current algorithm)
2. Team based (whole league, same team)
3. Tournament / Club Championships
4. Ladder
5. Interclub (League Ninja marketting excercise)


e.g. user flow


[set league mode]

[set players]
    |---> rank based auto flights (collect rank data first)

[set key dates]

X first contact 


Y follo up (SMS / email)


Deadline reminder

Deadline + auto scheduler

league kickoff

<div class="top-nav-dropdown">
                    Social Schedule Tool
                    <div class="dropdown-content">
                        {% for flight in current_user.club.flights %}
                        <a class="dropdown-item" href="{{ url_for('scheduler.social_schedule', flight_id=flight.id) }}">
                            {{ flight.flight_name }}
                        </a>
                        {% endfor %}
                    </div>
                </div>


''' 