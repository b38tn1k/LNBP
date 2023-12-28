from app.models import Model, db
from app.models import ModelProxy, transaction

class Player(Model):
    __tablename__ = 'player'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    contact_number = db.Column(db.String)
    communication_preference_mobile = db.Column(db.Boolean, default=False)
    communication_preference_email = db.Column(db.Boolean, default=False)
    gender = db.Column(db.String)
    club_ranking = db.Column(db.Integer, default=0) # could be inplemented via player ranking

    # Foreign Key for Club with cascading deletes
    club_id = db.Column(db.Integer, db.ForeignKey('club.id', ondelete='CASCADE'))

    # Relationship
    club = db.relationship('Club', backref=db.backref('players', lazy=True, cascade='all, delete-orphan'))

    GDPR_EXPORT_COLUMNS = {
        "id": "ID of the player",
        "email": "Player Email",
        "contact_number": "Player Contact Number",
        "communication_preference_mobile": "Player Mobile Communication Preference",
        "communication_preference_email": "Player Email Communication Preference",
        "created": "When the user was created",
        "first_name": "The players first name",
        "last_name": "The players last name",
        "gender": "The player gender",
        "club_ranking": "The player club ranking",
        "email_confirmed": "Whether the email was confirmation"
    }

    @property
    def full_name(self):
        """
        This function returns a string consisting of the first name and last name
        of the object passed to it separated by a space.

        Returns:
            str: The output returned by the `full_name()` function is an empty
            string ("") because the function doesn't have access to any attribute
            named `first_name` or `last_name`.

        """
        return f"{self.first_name} {self.last_name}"
    
    def in_flight(self, flight):
        """
        The `in_flight` function takes a `flight` object as an argument and returns
        a boolean value indicating whether the given flight is currently associated
        with any of the flight associations held by the object on which the function
        is called.

        Args:
            flight (): The `flight` input parameter is used to check if the
                associated object (e.g.

        Returns:
            bool: The output returned by this function is `True`.

        """
        return any(association.flight_id == flight.id for association in self.flight_associations)

    
    def __repr__(self):
        """
        This function defines a custom representation of an object for the
        `__repr__()` method.

        Returns:
            str: The output returned by this function is:
            
            "<Player undefined>"

        """
        return f'<Player {self.full_name}>'
