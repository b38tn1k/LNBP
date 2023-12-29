from app import db
from . import timeslot_court_association, Model
from .event import Event


class Timeslot(Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey("flight.id"))
    events = db.relationship("Event", backref="timeslot")
    # Many-to-many relationship with Court
    courts = db.relationship(
        'Court',
        secondary=timeslot_court_association,
        backref=db.backref('timeslots', lazy='dynamic'),
        lazy='dynamic'
    )

    def get_event_for_court_id(self, court_id):
        """
        This function retrieves the next event from a list of events for a given
        court ID.

        Args:
            court_id (int): The `court_id` input parameter specifies which event
                the function should return.

        Returns:
            None: The function `get_event_for_court_id` returns `None` because the
            comprehension `next((event for event ...` will only return a value if
            there exists an `event` that has a `court_id` equal to `court_id`, and
            since there are no such events the comprehension will not yield any values.

        """
        return next((event for event in self.events if event.court_id == court_id), None)

    def __repr__(self):
        """
        This function defines a `__repr__` special method for an object that is
        inheriting from something (hint: look at the `< Timeslot>` part).

        Returns:
            str: The output returned by this function is:
            
            "<Timeslot ...>".

        """
        return f"<Timeslot {self.start_time} - {self.end_time}>"
    
    def get_human_readable_date(self):
        # Format the start_time into a human-readable date string
        """
        This function takes an object of class `Whatever` and returns a human-readable
        date string consisting of the day name (in Uppercase), date and month
        (separated by a space), and time (in HH:MM AM/PM format) based on the
        `start_time` attribute of the object.

        Returns:
            str: The output returned by this function would be a string representing
            a human-readable date and time.

        """
        day_name = self.start_time.strftime("%A")  # Get the full day name (e.g., Monday)
        date_month = self.start_time.strftime("%B %d")  # Get the date and month (e.g., 25 July)
        time = self.start_time.strftime("%I:%M %p")  # Get the time in HH:MM AM/PM format
        return f"{day_name} {date_month}<br>{time}"
    
    def get_human_readable_day_number_month_year(self):
        """
        This function takes an object as input (which has a `start_time` attribute)
        and returns a human-readable representation of the date using the `strftime()`
        method.

        Returns:
            str: The output returned by the function `get_human_readable_day_number_month_year`
            is a string represented by "%A %m/%d/%Y".

        """
        return self.start_time.strftime("%A %m/%d/%Y")
    
    def get_human_readable_date_time_short(self):
        # Format the start_time into a human-readable date string
        """
        This function takes an object `self` and returns a string representing the
        date and time of `self.start_time` formatted as a human-readable date
        string with the day name (e.g., Monday), date (e.g., 25 July), and time
        (e.g., 14:30) separated by line breaks (`<br>`).

        Returns:
            str: The output returned by this function is a string that contains
            the day name (e.g., Monday), date and month (e.g., 25 July), and time
            (e.g., 14:30) separated by line breaks and an HTML br tag.

        """
        day_name = self.start_time.strftime("%A")  # Get the full day name (e.g., Monday)
        # date_month = self.start_time.strftime("%d/%m")  # Get the date and month (e.g., 25 July)
        date_month = self.start_time.strftime("%m/%d")  # Get the date and month (e.g., 25 July)
        time = self.start_time.strftime("%I:%M")  # Get the time in HH:MM AM/PM format
        return f"{day_name[0:3]}<br>{date_month}<br>{time}"
    
    def get_human_readable_date_day_month(self):
        # Format the start_time into a human-readable date string
        # day_name = self.start_time.strftime("%A")  # Get the full day name (e.g., Monday)
        # date_month = self.start_time.strftime("%B %d")  # Get the date and month (e.g., 25 July)
        """
        This function takes an object as input and returns a human-readable date
        string representing the day and month of the start time.

        Returns:
            str: The output returned by the function `get_human_readable_date_day_month`
            is a string representation of the start time of the event's day and
            month separated by a space (e.g., "25 July").

        """
        date_month = self.start_time.strftime("%m/%d")  # Get the date and month (e.g., 25 July)
        return date_month#f"{day_name} {date_month}"
    
    def get_human_readable_time(self):
        """
        This function takes an object as input (which has a `start_time` attribute)
        and returns a human-readable string representing the time using the AM/PM
        format. The string will have the format "HH:MM" (e.g.

        Returns:
            str: The output returned by this function is a string representing the
            time format HH:MM AM/PM (e.g., "12:30 PM").

        """
        time = self.start_time.strftime("%I:%M")  # Get the time in HH:MM AM/PM format
        return time
    
    def get_events(self): 
        """
        This function `get_events` returns a list of dictionaries where each
        dictionary represents an event and contains information such as the flight
        ID (`flight_id`), flight name (`flight_name`), time slot ID (`timeslot`),
        human-readable date and time (`readable_date` and `readable_time`), start
        time (`datetime_obj`), court ID (`court`), court name (`court_name`),
        players participating (`players` and `player_names`), and captain (`captain`
        and `captain_name`).

        Returns:
            dict: The output returned by this function is a list of dictionaries
            called `a`, where each dictionary represents an event and contains
            attributes such as flight ID (e.g.

        """
        a = []
        for e in self.events:
            if e.court:
                res = {}
                res['flight'] = self.flight_id
                res['flight_name'] = self.flight.flight_name
                res['timeslot'] = self.id
                res['readable_date'] = self.get_human_readable_day_number_month_year()
                res['readable_time'] = self.get_human_readable_time()
                res['datetime_obj'] = self.start_time
                res['court'] = e.court_id
                res['court_name'] = e.court.court_name
                res['players'] = []
                res['player_names'] = []
                res['captain'] = -1
                res['captain_name'] = "None"
                if e.captain:
                    res['captain'] = e.captain.id
                    res['captain_name'] = e.captain.player_name
                else:
                    res['captain'] = 34
                for p in e.players:
                    res['player_names'].append(p.player_name)
                    res['players'].append(p.id)
                a.append(res)
        return a
    
    def get_event_objects(self): 
        """
        This function takes no arguments and returns a list of all the event objects
        contained within the class's "events" attribute.

        Returns:
            list: The function returns the list `a`, which is empty because the
            `events` attribute of the object is not defined.

        """
        a = []
        for e in self.events:
            a.append(e)
        return a
    

    def delete_event_with_court_id(self, court_id):
        """
        This function deletes an event with the specified `court_id` from the list
        of events stored on the instance `self`, commits the changes to the database
        and returns `True` if the deletion was successful.

        Args:
            court_id (int): The `court_id` input parameter specifies the unique
                identifier of the court that the event belongs to and is used to
                filter out the desired event to be deleted from the list of events
                stored within the self.events list attribute.

        Returns:
            bool: The output returned by this function is `True`.

        """
        for e in self.events:
            if e.court_id == court_id:
                db.session.delete(e)
                #break
        db.session.commit()
        return True
    
    def get_court_by_id(self, court_id):
        """
        This function retrieves the first Court object from a list of Courts that
        have an id equal to the given court_id.

        Args:
            court_id (int): The `court_id` input parameter passes the ID of a
                specific court to be retrieved from the `courts` list.

        Returns:
            : The output returned by the `get_court_by_id` function is a single
            court object if there is one with the given ID within the `courts`
            list of the current instance.

        """
        return self.courts.filter_by(id=court_id).first()
    
    def delete_all_events(self, commit):
        """
        This function deletes all events associated with an object and optionally
        commits the changes to the database.

        Args:
            commit (bool): The `commit` input parameter indicates whether to commit
                the changes made by the function after deleting all events. If
                `commit` is set to `True`, the changes will be committed and written
                to the database.

        """
        for e in self.events:
            db.session.delete(e)
        if commit:
            db.session.commit()

    def on_delete(self):
        """
        This function calls the `delete_all_events` method with `False` as an
        argument to delete all events associated with the instance.

        """
        self.delete_all_events(False)
    
    def create_event(self, court, players, captain=None):
        # Filter existing events using Python's built-in filter function
        """
        This function creates a new event or updates an existing one based on the
        provided court and players. If an existing event with the same court and
        players is found. It returns the ID of the existing event. If no matching
        event is found.

        Args:
            court (str): The `court` input parameter specifies the court where the
                event will take place.
            players (list): The `players` input parameter is a list of players to
                be included In the event that is being created or updated.
            captain (): The `captain` input parameter specifies the player who
                will be the captain of the event. If a matching event is found
                based on the `court` and `players`, the captain of the found event
                will be set to the provided `captain`. If no matching event is
                found and a new event is created instead.

        Returns:
            int: The output returned by this function is either the ID of an
            existing event that matches the given court and players or a newly
            created event object if no matching event is found.

        """
        matching_events = list(filter(
            lambda e: e.court == court and e.captain == captain, 
            self.events
        ))

        # Find the first event with matching players, if any
        existing_event = None
        for event in matching_events:
            existing_player_ids = {player.id for player in event.players}
            new_player_ids = {player.id for player in players}
            if existing_player_ids == new_player_ids:
                existing_event = event
                break

        # If a matching event is found, return its ID
        if existing_event:
            return existing_event.id

        # If no matching event is found, create a new one
        event = Event(timeslot=self, court=court, captain=captain)
        for player in players:
            event.players.append(player)
        
        db.session.add(event)
        db.session.commit()
        return event.id
