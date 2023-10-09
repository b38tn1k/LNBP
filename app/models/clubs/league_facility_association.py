from app.models import db, Model

class LeagueFacilityAssociation(Model):
    __tablename__ = 'league_facility_association'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign keys for League and Facility with cascading deletes
    league_id = db.Column(db.Integer, db.ForeignKey('league.id', ondelete='CASCADE'))
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id', ondelete='CASCADE'))

    # Relationships
    league = db.relationship('League', backref=db.backref('facility_associations', lazy=True, cascade='all, delete-orphan'))
    facility = db.relationship('Facility', backref=db.backref('league_associations', lazy=True, cascade='all, delete-orphan'))
    
    GDPR_EXPORT_COLUMNS = {}
