from . import flight_player_association, Model
from datetime import datetime
from app import db
import json

from sqlalchemy.dialects.postgresql import JSON


class Player(Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(64), index=True)
    player_email = db.Column(db.String(64), index=True, default='')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id', name='player_admined_club'))
    club = db.relationship('Club', backref='players')
    flights = db.relationship(
        'Flight',
        secondary=flight_player_association,
        lazy='dynamic',
        viewonly=True
    )
    availability_data = db.Column(JSON)
        
    def get_availability_obj_for_flight(self, flight_id):
        """
        This function gets an availability object for a flight by retrieving it
        from a dictionary of flight availability data stored as a JSON string.

        Args:
            flight_id (str): The `flight_id` input parameter is used to identify
                the specific flight for which the availability information is requested.

        Returns:
            dict: The output returned by this function is `None`.

        """
        if self.availability_data:
            # Parse the JSON string into a dictionary
            try:
                availability_data_dict = json.loads(self.availability_data)
            except json.JSONDecodeError:
                # Handle the exception if JSON decoding fails
                print(f"Failed to decode JSON for availability_data: {self.availability_data}")
                return None

            # Check if the flight_id exists in the dictionary
            if str(flight_id) in availability_data_dict:
                return availability_data_dict[str(flight_id)]
        return None
        
    def remove_availability_for_flight(self, flight_id):
        """
        This function removes availability information for a specific flight by
        removing the given flight ID from the internal availability data dictionary
        if it exists.

        Args:
            flight_id (str): The `flight_id` input parameter is used to identify
                the specific flight for which availability should be removed from
                the availability data.

        Returns:
            bool: The output returned by this function is `False`.

        """
        if self.availability_data and str(flight_id) in self.availability_data:
            # self.availability_data[str(flight_id)] = '' # this should be better
            return True
        else:
            return False

    def __repr__(self):
        """
        This function defines the representation (or repr) of an object of class
        Player.

        Returns:
            str: The output returned by this function is '<Player undefined>'.

        """
        return '<Player {}>'.format(self.player_name)
