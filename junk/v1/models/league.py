from app import db
from .player import Player
from .court import Court
from .flight import Flight
from . import Model

def generate_scorecard_from_event(e, fields):
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
        check = Flight.query.filter_by(flight_name=flight_name, league=self).first()
        if check is None:
            flight = Flight(flight_name=flight_name, league=self)
            db.session.add(flight)
            if commit:
                db.session.commit()
            return flight
        return check
    
    def delete(self, commit=True):
        for f in self.flights:
            f.on_delete()
            db.session.delete(f)
        db.session.delete(self)
        if commit:
            db.session.commit()
        return True

    def get_events_sorted(self):
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
        scorecards = []
        fields = ['1st Set', '2nd Set', '3rd Set', 'Games Won', 'Games Lost', 'Sets Won', 'W-L Adjusted']
        events = self.get_events_sorted()
        for e in events:
            scorecards.append(generate_scorecard_from_event(e, fields))
        result = "\n\n".join(scorecards)
        return result
    
    def generate_schedule_CSV(self):
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