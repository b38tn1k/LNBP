from app.models import Model, db

class Facility(Model):
    __tablename__ = 'facility'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    asset_type = db.Column(db.String)  # Type of the facility. E.g., "Tennis Court", "Swimming Pool", etc.
    asset_description = db.Column(db.String(100))
    location_description = db.Column(db.String(100))
    name = db.Column(db.String)

    # Foreign Key for Club with cascading deletes
    club_id = db.Column(db.Integer, db.ForeignKey('club.id', ondelete='CASCADE'))

    # Relationship
    club = db.relationship('Club', backref=db.backref('facilities', lazy=True, cascade='all, delete-orphan'))

    # # Relationship for User administrators
    # administrators = db.relationship('FacilityAdministrator', back_populates='facility')

    GDPR_EXPORT_COLUMNS = {}

    def __repr__(self):
        return f'<Facility {self.id} - {self.name}>'
    
    @staticmethod
    def create(name, asset_type, club):
        facility = Facility(name=name, asset_type=asset_type, club=club)
        db.session.add(facility)
        db.session.commit()
        return facility
