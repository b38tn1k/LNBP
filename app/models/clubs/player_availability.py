from app.models import db, Model

class PlayerAvailability(Model):
    __tablename__ = 'player_availability'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    availability = db.Column(db.Integer)

    # Foreign keys for LeaguePlayerAssociation and Timeslot with cascading deletes
    association_id = db.Column(db.Integer, db.ForeignKey('league_player_association.id', ondelete='CASCADE'))
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslot.id', ondelete='CASCADE'))

    # Relationships
    association = db.relationship('LeaguePlayerAssociation', backref=db.backref('availability_associations', lazy=True, cascade='all, delete-orphan'))
    timeslot = db.relationship('Timeslot', backref=db.backref('availability_associations', lazy=True, cascade='all, delete-orphan'))
