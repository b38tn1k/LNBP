from app.models import Model, db

class FacilityAdministrator(Model):
    __tablename__ = 'facility_administrator'

    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    
    # Note: The string representations 'Facility' and 'User' in the relationships
    facility = db.relationship('Facility', back_populates='administrators')
    user = db.relationship('User', back_populates='administered_facilities')

    GDPR_EXPORT_COLUMNS = {}
