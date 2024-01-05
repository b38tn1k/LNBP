from app.models import db, Model

# Create an intermediary table to represent the many-to-many relationship
game_event_player_association = db.Table(
    'game_event_player_association',
    db.Column('game_event_id', db.Integer, db.ForeignKey('league_game_event.id')),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
)

class LeagueGameEvent(Model):
    __tablename__ = 'league_game_event'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys for League, Facility, Flight, and Timeslot with cascading deletes
    captain_id = db.Column(db.Integer, db.ForeignKey('player.id', ondelete='CASCADE'), nullable=True)
    league_id = db.Column(db.Integer, db.ForeignKey('league.id', ondelete='CASCADE'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id', ondelete='CASCADE'))
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id', ondelete='CASCADE'))
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslot.id', ondelete='CASCADE'))

    # Relationships
    flight = db.relationship('Flight', backref=db.backref('game_events', lazy=True, cascade='all, delete-orphan'))
    league = db.relationship('League', backref=db.backref('game_events', lazy=True, cascade='all, delete-orphan'))
    facility = db.relationship('Facility', backref=db.backref('game_events', lazy=True, cascade='all, delete-orphan'))
    timeslot = db.relationship('Timeslot', backref=db.backref('game_events', lazy=True, cascade='all, delete-orphan'))
    captain = db.relationship('Player', backref=db.backref('captained_games', lazy=True, cascade='all, delete-orphan'))

    # Define the many-to-many relationship with players
    players = db.relationship('Player', secondary=game_event_player_association, backref=db.backref('game_events', lazy=True))

    GDPR_EXPORT_COLUMNS = {}

    def get_players(self):
        """
        This function returns a list of all players stored within the instance's
        `players` attribute.

        Returns:
            list: The function `get_players()` returns a list of players (`[player
            for player...]` is a list comprehension that creates a list of all
            players stored within `self.players`).

        """
        return [player for player in self.players]
        

    def __repr__(self):
        """
        This function defines a special method named `__repr__` (short for
        "representation") that takes an object of class `LeagueGameEvent` and
        returns a string representation of the object.

        Returns:
            str: The output returned by this function is a string:
            
            "<LeagueGameEvent(id=,..., players=[...])>".

        """
        players = [player for player in self.players]
        return f"<LeagueGameEvent(id={self.id}, captain_id={self.captain_id}, " \
               f"league_id={self.league_id}, flight_id={self.flight_id}, " \
               f"facility_id={self.facility_id}, timeslot_id={self.timeslot_id}, " \
               f"players={players})>"
