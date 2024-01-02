from app.models import db, Model

class LeagueGameEvent(Model):
    __tablename__ = 'league_game_event'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    is_captain = db.Column(db.Boolean, default=False)

    # Foreign keys for League, Player, Facility, and Timeslot with cascading deletes
    league_id = db.Column(db.Integer, db.ForeignKey('league.id', ondelete='CASCADE'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id', ondelete='CASCADE'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id', ondelete='CASCADE'))
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id', ondelete='CASCADE'))
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslot.id', ondelete='CASCADE'))

    # Relationships
    flight = db.relationship('Flight', backref=db.backref('game_events', lazy=True, cascade='all, delete-orphan'))
    league = db.relationship('League', backref=db.backref('game_events', lazy=True, cascade='all, delete-orphan'))
    player = db.relationship('Player', backref=db.backref('game_events', lazy=True, cascade='all, delete-orphan'))
    facility = db.relationship('Facility', backref=db.backref('game_events', lazy=True, cascade='all, delete-orphan'))
    timeslot = db.relationship('Timeslot', backref=db.backref('game_events', lazy=True, cascade='all, delete-orphan'))

    GDPR_EXPORT_COLUMNS = {}
