from app.models import db, Model

class Club(Model):
    __tablename__ = 'club'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    contact_number = db.Column(db.String(50))  # Assuming phone number format suits a max length of 50
    street_address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))  # Assuming state name or abbreviation
    zip_code = db.Column(db.String(15))  # Adjust length based on the country's ZIP/Postal code format
    country = db.Column(db.String(100))

    GDPR_EXPORT_COLUMNS = {
        "id": "ID of the club",
        "email": "Club Email",
        "contact_number": "Club Contact Number",
        "street_address": "Club Street Address",
        "city": "Club City",
        "state": "Club state / region / province",
        "zip_code": "Club postal code",
        "country": "Club country",
    }

    @staticmethod
    def create(name):
        club = Club(name=name)
        db.session.add(club)
        db.session.commit()
        return club

    # Relationships and other methods as required

    # ... other attributes and methods ...

    def __repr__(self):
        return '<Club {0} - {1}>'.format(self.id, self.name)
