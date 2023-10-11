from app.models import Model, db

class FacilityAdministrator(Model):
    __tablename__ = 'facility_administrator'

    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    
    # Relationships with backrefs
    facility = db.relationship('Facility', backref=db.backref('administrators', lazy=True, cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('administered_facilities', lazy=True, cascade='all, delete-orphan'))

    GDPR_EXPORT_COLUMNS = {}

    @staticmethod
    def create(user, facility):
        FA = FacilityAdministrator(user=user, facility=facility)
        db.session.add(FA)
        db.session.commit()
        return FA
