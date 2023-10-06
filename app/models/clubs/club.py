from app.models import db, Model

class Club(Model):
    __tablename__ = 'club'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))  # Assuming phone number format suits a max length of 50
    street_address = db.Column(db.String(255))
    state = db.Column(db.String(100))  # Assuming state name or abbreviation
    zip_code = db.Column(db.String(15))  # Adjust length based on the country's ZIP/Postal code format
    country = db.Column(db.String(100))

    # Relationships and other methods as required

    # ... other attributes and methods ...

    def __repr__(self):
        return '<Club {0} - {1}>'.format(self.id, self.name)
