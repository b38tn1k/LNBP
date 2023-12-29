from .timeslot import Timeslot
from . import flight_player_association, Model
from app import db
import json


class Flight(Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_name = db.Column(db.String(64), index=True)
    league_id = db.Column(db.Integer, db.ForeignKey('league.id', name='admined_league'))
    league = db.relationship('League', backref='flights')
    timeslots = db.relationship('Timeslot', backref='flight', lazy='dynamic')
    bg_color = db.Column(db.String(7), default='#000000')
    fg_color = db.Column(db.String(7), default='#ffffff')
    players = db.relationship(
        'Player',
        secondary=flight_player_association,
        lazy='dynamic'
    )

    def print_timeslots_and_events(self):
        """
        This function prints the number of timeslots and the number of events
        associated with each timeslot for a given flight name.

        """
        total_timeslots = self.timeslots.count()
        print(f"Total timeslots in {self.flight_name}: {total_timeslots}")

        for timeslot in self.timeslots:
            num_events = len(timeslot.events)
            print(f"Timeslot {timeslot.id} (from {timeslot.start_time} to {timeslot.end_time}): {num_events} events")

    def on_delete(self):
        """
        The `on_delete` function is a trigger that runs when the instance of the
        class is deleted (i.e., when the object is torn down or garbage collected).

        """
        self.clean_players(False)
        self.delete_timeslots(False)

    def get_other_court_events(self):
        """
        This function retrieves a list of colliding events (i.e., events that
        cannot be scheduled at the same time) for a given timeslot and court by
        querying each court's scheduling system and combining the results.

        Returns:
            list: The function "get_other_court_events" returns a list of colliding
            events for a given timeslot and court id.

        """
        collisions = []
        for timeslot in self.timeslots:
            for court in timeslot.courts:
                res = court.get_colliding_events(timeslot, self.id)
                for r in res:
                    collisions.append(r)
        return collisions

    def get_all_courts(self):
        """
        Get a sorted list of all courts used in the flight's timeslots.
        """
        all_courts = set()  # Use a set to collect unique courts
        for timeslot in self.timeslots:
            all_courts.update(timeslot.courts)  # Use 'update' to add elements to the set
        return sorted(all_courts, key=lambda court: court.court_name)

    def get_flight_dimensions(self):
        """
        This function `get_flight_dimensions` returns an array of two elements
        representing the dimensions (number of rows and number of columns) of a
        table or matrix of 'timeslots' (either list of lists or dictionary of
        dictionaries) by iterating through each item/dictionary and finding the
        maximum number of courts (or columns) and storing it for that particular
        row/index.

        Returns:
            int: The function returns the array `[3]` with one element `3`.

        """
        y = len(self.timeslots)
        x = 0
        for timeslot in self.timeslots.all():
            if len(timeslot.courts > x):
                x = len(timeslot.courts)
        return [x, y]

    def add_player(self, player):
        """
        This function adds a new player to a list of players stored on an object
        called "self".

        Args:
            player (): The `player` input parameter is passed to the function as
                an object to be appended to the `self.players` list.

        """
        if player not in self.players:
            self.players.append(player)
            db.session.commit()

    def remove_player(self, player):
        """
        The given function "remove_player" takes a player object as an argument
        and removes it from the list of players stored by the object's attribute
        "players".

        Args:
            player (): The `player` input parameter is used to identify the player
                to be removed from the list of players stored on the object.

        """
        if player in self.players:
            self.players.remove(player)
            db.session.commit()

    def player_in_flight(self, player):
        """
        This function checks if a given `player` object is contained within the
        `self.players` list.

        Args:
            player (list): The `player` input parameter is passed as an object to
                be checked against the `self.players` list to determine if the
                player is currently logged into the game.

        Returns:
            bool: The output returned by this function is `False`.

        """
        return player in self.players

    def generate_schedule_CSV(self):
        """
        This function generates a CSV string representation of a schedule for a
        tennis tournament. It appends header rows to the CSV string representing
        the flight name and date for each timeslot and the human-readable time for
        each timeslot. Then it iterates over each player and generates a row for
        each player with their player name and the court names for each timeslot
        they are assigned to.

        Returns:
            str: The output returned by this function is a string representing a
            CSV file with four columns: flight name (first column), human-readable
            date and time (second column), captain information (third column), and
            court name (fourth column).

        """
        csv_list = []

        header1 = []
        header1.append(self.flight_name)
        for timeslot in self.get_sort_timeslots():
            header1.append(timeslot.get_human_readable_date_day_month())
        csv_list.append(header1)

        header2 = [" "]
        for timeslot in self.get_sort_timeslots():
            header2.append(timeslot.get_human_readable_time())
        csv_list.append(header2)

        for player in self.players:
            player_row = [player.player_name]
            for timeslot in self.get_sort_timeslots():
                game = ''
                events = timeslot.get_events()
                for e in events:
                    # print(e)
                    if e['captain'] == player.id:
                        game += "C"
                    if player.id in e['players']:
                        game += e['court_name']
                player_row.append(game)
            csv_list.append(player_row)

        rows = []
        for row in csv_list:
            rows.append(', '.join(row))
        csv = '\n'.join(rows)
        return csv
    
    def get_player_availability(self):
        """
        This function gets the availability of each player for a specific flight
        by querying their availability objects and storing the results as a
        dictionary where the keys are player IDs and values are availability objects.

        Returns:
            dict: The output returned by the `get_player_availability` function
            is a dictionary where each key is a player ID and each value is the
            corresponding player's availability for the flight with ID `self.id`.

        """
        a = {}
        for player in self.players:
            avail = player.get_availability_obj_for_flight(self.id)
            a[player.id] = avail
        return a
    
    def get_events(self):
        """
        This function `get_events` retrieves all events associated with each time
        slot and appends them to a list called `a`.

        Returns:
            list: The function `get_events` returns a list of all events associated
            with all Timeslots objects.

        """
        a = []
        for timeslot in self.timeslots.all():
            es = timeslot.get_events()
            for e in es:
                a.append(e)
        return a

    def get_event_objects(self):
        """
        This function "get_event_objects" retrieves all the event objects associated
        with each timeslot object within the current instance of the class
        "Timeslots", and returns a list containing all the retrieved event objects.

        Returns:
            list: The output of the `get_event_objects()` function is a list of
            `EventObject` objects called `a`, which is constructed by iterating
            over each ` timeslot` object's `get_event_objects()` method and appending
            the returned events to the list `a`.

        """
        a = []
        for timeslot in self.timeslots.all():
            es = timeslot.get_event_objects()
            for e in es:
                a.append(e)
        return a

    def __repr__(self):
        """
        This function defines a custom `__repr__` (representation) method for an
        object of class `Flight`.

        Returns:
            str: The output returned by this function is: '<Flight >'.

        """
        return '<Flight {}>'.format(self.flight_name)
    
    def delete_timeslots(self, commit=True):
        """
        This function deletes all the instances of `Timeslot` objects attached to
        an object of type `self`, by calling their `__on_delete__` method and then
        deleting them from the database if commit is True.

        Args:
            commit (bool): The `commit` parameter is an optional argument to the
                `delete_timeslots` function that determines whether to commit the
                deletion immediately or not.

        """
        for timeslot in self.timeslots.all():
            timeslot.on_delete()
            db.session.delete(timeslot)
        if commit:
            db.session.commit()

    def delete_events(self):
        """
        This function deletes all events associated with each timeslot object and
        commits the changes to the database.

        """
        for timeslot in self.timeslots.all():
            timeslot.delete_all_events(False)
        db.session.commit()
    
    def create_timeslot(self, start_time, end_time, courts):
        # Search for a timeslot in flight.timeslots with matching start and end times
        """
        This function creates a new Timeslot object and assigns it to a flight
        object if no matching timeslot is found or else returns the existing
        timeslot id.

        Args:
            start_time (): The `start_time` input parameter specifies the starting
                time of the desired timeslot.
            end_time (): The `end_time` input parameter specifies the end time of
                the desired timeslot.
            courts (list): The `courts` input parameter is a list of court objects
                that are associated with the created timeslot.

        Returns:
            int: The output returned by this function is an ID.

        """
        matching_timeslot = next((ts for ts in self.timeslots if ts.start_time == start_time and ts.end_time == end_time), None)

        if matching_timeslot is None:
            timeslot = Timeslot(start_time=start_time, end_time=end_time, flight=self)
            for court in courts:
                timeslot.courts.append(court)
            db.session.add(timeslot)
            db.session.commit()
            return timeslot.id

        return matching_timeslot.id

    def get_sort_timeslots(self):
        """
        This function takes an object of a class with a `timeslots` attribute that
        is a list of dictionaries representing time slots with a `start_time` key.

        Returns:
            list: The output returned by this function is a list of `Timeslot`
            objects sorted by their start time (as represented as a string of the
            form "20YY-MM-DDTHH:MI:SS" with the seconds fraction omitted).

        """
        return sorted(self.timeslots, key=lambda x: x.start_time.isoformat()[5:10])
    
    def clean_players(self, commit=True):
        """
        The `clean_players` function removes the availability of all players for
        the given flight from the database and commits any changes if the `commit`
        parameter is set to `True`.

        Args:
            commit (bool): The `commit` parameter is an optional keyword argument
                that determines whether to immediately commit any changes made to
                the database within the scope of the function.

        """
        for player in self.players:
            player.remove_availability_for_flight(self.id)
        if commit:
            db.session.commit()

    def get_timeslots_json(self):
        """
        This function retrieves a list of dictionaries representing available
        timeslots and their corresponding courts' IDs for display on a schedule.
        It uses the `get_sort_timeslots` method to retrieve the timeslots and then
        loops through each timeslot to create a dictionary with its properties
        like start/end time and background color and appends it to a list of dictionaries.

        Returns:
            dict: The output returned by this function is a JSON object list.

        """
        timeslots_list = []
        for timeslot in self.get_sort_timeslots():
            court_ids = [court.id for court in timeslot.courts.all()]
            # TODO need to check if court is already busy!
            timeslot_dict = {
                'id': timeslot.id,
                'title': timeslot.flight.flight_name,
                'start': timeslot.start_time.isoformat(),
                'end': timeslot.end_time.isoformat(),
                'display': 'block',
                'backgroundColor': self.bg_color,
                'textColor': self.fg_color,
                'courts': court_ids,
            }
            timeslots_list.append(timeslot_dict)
        return json.dumps(timeslots_list)
    
    # method to get timeslot by id
    def get_timeslot_by_id(self, timeslot_id):
        """
        This function retrieves the first `Timeslot` object from a list of `Timeslots`
        that matches the given `timeslot_id`.

        Args:
            timeslot_id (int): The `timeslot_id` parameter is used to retrieve a
                specific `Timeslot` object from the `self.timeslots` list based
                on its ID.

        Returns:
            : The output of this function is a `Timeslot` object representing the
            timeslot with the given `timeslot_id`, or `None` if no such timeslot
            exists.

        """
        return self.timeslots.filter_by(id=timeslot_id).first()

    # method to get player by id
    def get_players_by_id(self, player_id):
        """
        This function `get_players_by_id` retrieves the first player from a queryset
        (`self.players`) that has the given `player_id`.

        Args:
            player_id (int): The `player_id` input parameter specifies the unique
                identifier of the player to retrieve from the list of players.

        Returns:
            : The output returned by the function `get_players_by_id` is either a
            single `Player` object if there is one match for the given `player_id`,
            or `None` if no match is found.

        """
        return self.players.filter_by(id=player_id).first()

