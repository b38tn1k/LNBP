from app.models import db, Model
from datetime import datetime, timedelta

class Timeslot(Model):
    __tablename__ = 'timeslot'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    # Foreign Key for League
    league_id = db.Column(db.Integer, db.ForeignKey('league.id', ondelete='CASCADE'))

    # Relationship to League
    league = db.relationship('League', backref=db.backref('timeslots', lazy=True, cascade='all, delete-orphan'))

    GDPR_EXPORT_COLUMNS = {}

    def __repr__(self):
        """
        This function defines a `__repr__` method for a `Timeslot` object.

        Returns:
            str: The output returned by the function is:
            
            <Timeslot - Thu 14:30>

        """
        return f'<Timeslot - {self.human_readable_hhmm_dayname_mdy()}>'
    
    @property
    def since_y2k(self):
        """
        This property returns a dictionary containing the number of days and weeks since Y2K (January 1, 2000),
        calculated from the start time of the timeslot.

        Returns:
            dict: A dictionary with keys 'days' and 'weeks', representing the number of days and weeks since Y2K.
        """
        y2k = datetime(2000, 1, 1)
        delta = self.start_time - y2k  # Calculate the timedelta from Y2K to the start_time
        days = delta.days  # Number of days since Y2K
        weeks = days // 7  # Number of weeks since Y2K

        return {'days': days, 'weeks': weeks}
    
    def check_overlap(self, other_timeslot):
        """
        Checks if there is any overlap between this timeslot and another timeslot.

        Args:
            other_timeslot (Timeslot): Another Timeslot object to check for overlap.

        Returns:
            bool: True if there is overlap, False otherwise.
        """
        # Check if one timeslot starts during the other
        return (self.start_time < other_timeslot.end_time and self.end_time > other_timeslot.start_time) \
            or (other_timeslot.start_time < self.end_time and other_timeslot.end_time > self.start_time)


    def human_readable_hhmm_mdy(self):
        """
        This function takes an object 'self' and returns a human-readable
        representation of the start time field as a string formatted as '%H:%M %m/%d/%Y'.

        Returns:
            str: The output returned by the function `human_readable_hhmm_mdy`
            would be:
            
            "14:30 03/02/2023"

        """
        return self.start_time.strftime('%H:%M %m/%d/%Y')

    def human_readable_hhmm_dayname_mdy(self):
        """
        This function returns a human-readable string representing the current day
        and time based on the 'start_time' attribute of the object.

        Returns:
            str: The output returned by the `human_readable_hhmm_dayname_mdy`
            function is a string representation of the current date and time using
            the format "%H:%M %A %m/%d/%Y".

        """
        return self.start_time.strftime('%H:%M %A %m/%d/%Y')

    def human_readable_hhmm(self):
        """
        This function returns a human-readable representation of the start time
        of an object using the hh:mm format (e.g., "14:30" for 2:30 PM).

        Returns:
            str: The output returned by the `human_readable_hhmm` function is `0:00`.

        """
        return self.start_time.strftime('%H:%M')

    def human_readable_dayname_monthname(self):
        """
        This function returns the human-readable day and month name based on the
        start time of an object represented by 'self', using the strftime() method.

        Returns:
            str: The output returned by this function is "Sunday February" because
            %A represents the day of the week as a three-letter abbreviation and
            %B represents the month as a three-letter abbreviation.

        """
        return self.start_time.strftime('%A %B')

    def human_readable_hhmm_mmdd(self):
        """
        The function `human_readable_hhmm_mmdd` returns a human-readable string
        representation of the current timestamp using the format `'%H:%M %m/%d'`.

        Returns:
            str: The output returned by the function `human_readable_hhmm_mmdd`
            is `'%H:%M %m/%d'`.

        """
        return self.start_time.strftime('%H:%M %m/%d')
    
    def human_readable_mmdd_hhmm(self):
        """
        The function "human_readable_mmdd_HHMM" converts a Timestamp object (self)
        into a human-readable format displaying the date and time as "mm/dd HH:MM".

        Returns:
            str: The output returned by the `human_readable_mmdd_HHMM` function
            is a string representing the start time of an event as a human-readable
            format: e.g.

        """
        return self.start_time.strftime('%a %m/%d %H:%M')
    
    def get_duration(self):
        """
        This function takes an object of a class as an input and returns the
        duration of the object (in minutes) based on the start and end times of
        the object.

        Returns:
            int: The output returned by the function `get_duration` would be the
            number of minutes spent on the event.
            
            For example:
            
            If `self.start_time` is `2023-03-06 10:00:00` and `self.end_time` is
            `2023-03-06 11:00:00`, then the duration would be `1 hour` or `60 minutes`.
            
            So the function would return `60`.

        """
        duration = self.end_time - self.start_time
        return int(duration.total_seconds() / 60)
