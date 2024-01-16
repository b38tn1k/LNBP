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
        """
        This function defines a custom repr method for a Facility object.

        Returns:
            str: The output returned by the `__repr__` function is:
            
            '`<Facility [ id=..., name=...

        """
        return f'<Facility {self.id} - {self.name}>'
    
    @staticmethod
    def create(name, asset_type, club):
        """
        This function creates a new instance of the `Facility` class and adds it
        to the database.

        Args:
            name (str): The `name` input parameter is used to set the name of the
                Facility object that will be created.
            asset_type (str): The `asset_type` input parameter specifies the type
                of asset being created (e.g.
            club (str): The `club` input parameter is used to specify which club
                the facility will belong to.

        Returns:
            : The output returned by this function is a Facility object named 'facility'.

        """
        facility = Facility(name=name, asset_type=asset_type, club=club)
        db.session.add(facility)
        db.session.commit()
        return facility
    
    def is_available(self, t):
        """
        This function checks whether a given time `t` is available for a game event
        by checking if there is any conflict with existing game events on the same
        day.

        Args:
            t (): In the function `is_available`, `t` is a Time object and serves
                as the input parameter that specifies the time to be checked for
                availability.

        Returns:
            bool: The function takes an argument `t` and returns `True` if there
            is no overlap between `t` and any of the game events stored In the
            object's `game_events` list.

        """
        day_number = t.since_y2k['days']
        for g in self.game_events:
            if day_number == g.timeslot.since_y2k['days']:
                if t.check_overlap(g.timeslot):
                    return False
        return True

