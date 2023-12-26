from app.models import db, Model
from app.models import ModelProxy, transaction

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
    @transaction
    def add_facility(self, name, asset_type, user, club):
        facility = ModelProxy.clubs.Facility.create(name, asset_type, club)
        facility_admin = ModelProxy.clubs.FacilityAdministrator(user=user, facility=facility)
        print(user.club.facilities)
        return facility
    
    @transaction
    def create_league(self, name, league_type, start_date, end_date, add=True, commit=False):
        """
        Create a new league associated with this club.

        :param name: Name of the league.
        :param league_type: Type of the league.
        :param start_date: Start date of the league.
        :param bg_color: Background color of the league.
        :param fg_color: Foreground color of the league.
        :return: Created League instance.
        """
        # Create a new League instance
        new_league = ModelProxy.clubs.League(name=name, type=league_type, 
                                             start_date=start_date, end_date=end_date, club=self)

        if add is True:
            db.session.add(new_league)
        if commit is True:
            db.session.commit()

        return new_league

    def __repr__(self):
        return '<Club {0} - {1}>'.format(self.id, self.name)
