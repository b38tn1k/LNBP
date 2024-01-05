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
