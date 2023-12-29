from app.models import db, Model

class FlightPlayerAssociation(Model):
    __tablename__ = 'flight_player_association'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign keys for League and Player with cascading deletes
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id', ondelete='CASCADE'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id', ondelete='CASCADE'))

    # Relationships
    flight = db.relationship('Flight', backref=db.backref('player_associations', lazy=True, cascade='all, delete-orphan'))
    player = db.relationship('Player', backref=db.backref('flight_associations', lazy=True, cascade='all, delete-orphan'))

    GDPR_EXPORT_COLUMNS = {}