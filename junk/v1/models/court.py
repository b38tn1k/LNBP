from app import db
import json
from . import Model


class Court(Model):
    id = db.Column(db.Integer, primary_key=True)
    court_name = db.Column(db.String(64), index=True)
    club_id = db.Column(db.Integer, db.ForeignKey("club.id", name="court_admined_club"))
    club = db.relationship("Club", backref="courts")

    def __repr__(self):
        """
        This function defines the object's representation (repr) as a string that
        displays the object's court name.

        Returns:
            str: The output returned by this function is "<Court {}>".

        """
        return "<Court {}>".format(self.court_name)

    def get_timeslots_json(self):
        """
        This function returns a JSON string representing an array of objects
        containing information about available time slots for a specific flight.
        Each object contains properties such as "id", "title", "start" and "end"
        timestamps.

        Returns:
            str: The output returned by this function is a JSON object representing
            the list of `Timeslot` objects as a list of dictionaries.

        """
        timeslots_list = []
        for timeslot in self.timeslots:
            timeslot_dict = {
                "id": timeslot.id,
                "title": timeslot.flight.flight_name,
                "start": timeslot.start_time.isoformat(),
                "end": timeslot.end_time.isoformat(),
                "display": "block",
                "backgroundColor": timeslot.flight.bg_color,
                "textColor": timeslot.flight.fg_color,
            }
            timeslots_list.append(timeslot_dict)
        return json.dumps(timeslots_list)

    def get_available(self, timeslot):
        """
        This function checks if the given timeslot is present inside the
        `self.timeslots` list of the object.

        Args:
            timeslot (str): The `timeslot` input parameter is passed as an argument
                to the `get_available` function and is used to check if a specific
                time slot is available or not.

        Returns:
            bool: The output returned by the function `get_available` is `True`
            if the input `timeslot` is present as a key (value: `None`) within the
            `.timeslots` attribute of the instance of the class it's defined within;
            otherwise (if timeslot is not present) the function returns `False`.

        """
        return timeslot in self.timeslots

    def get_colliding_events(self, timeslot, lid):
        """
        This function gets all events that collide with a given timeslot and return
        the collided events as a list of dictionaries containing "court_id",
        "timeslot_id" and "flight_name".

        Args:
            timeslot (): The `timeslot` input parameter specifies the target
                timeslot to check for collisions with the events.
            lid (int): The `lid` input parameter specifies the ID of the flight
                for which the events should be checked for conflicts.

        Returns:
            dict: The output of this function is a list of dictionaries containing
            information about the collisions between events and timeslots.

        """
        collisions = []
        for event in self.events:
            if not event.timeslot:
                db.session.delete(event)
                db.session.commit()
            if lid and event.timeslot:
                if event.timeslot.flight.id != lid:
                    event_start = event.timeslot.start_time
                    event_end = event.timeslot.end_time

                    timeslot_start = timeslot.start_time
                    timeslot_end = timeslot.end_time
                    if (
                        event_start >= timeslot_start and event_start < timeslot_end
                    ) or (event_end >= timeslot_start and event_end < timeslot_end):
                        collisions.append(
                            {
                                "court_id": self.id,
                                "timeslot_id": timeslot.id,
                                "flight_name": event.timeslot.flight.flight_name,
                            }
                        )
        return collisions
