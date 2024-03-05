from app.models import db, Model
from datetime import datetime, timedelta
from app.models import ModelProxy, transaction


def construct_schedule_string(day_counter, time_counter):
    # Calculate the average counts
    """
    This function constructs a sentence that summarizes a sports team's schedule
    for the day. It takes two dictionaries as input: one with the number of games
    played on each day of the week (represented as integers), and another with the
    number of times each game was played at each time (represented as integers).
    The function calculates the average number of games per day and time and uses
    that information to create a string representing the schedule.

    Args:
        day_counter (dict): The `day_counter` input parameter is a dictionary that
            keeps track of how many times each day of the week (i.e. "Monday",
            "Tuesday", etc.) appears as a game date.
        time_counter (dict): The `time_counter` input parameter is a dictionary
            of counts for each time slot.

    Returns:
        str: The output returned by the `construct_schedule_string` function is a
        string representing the team's schedule. Here's an example:
        
        Suppose we have the following dicts `day_counter` and `time_counter`:
        ```python
        day_counter = {
            "Monday": 20.,
            "Tuesday": 15.,
            "Wednesday": 25.,
            "Thursday": 10.
        }
        
        time_counter = {
            "16:00": 30.,
            "17:00": 15.,
            "18:00": 10.,
            "19:00": 5.
        }
        ```
        Then running `construct_schedule_string(day_counter=day_counter',
        time_counter=time_counter)` would return the following schedule string:
        ```text
        Monday. Games at 16:00 and 18:00 evenings. Tuesday. Games at 17:00 Wednesday.
        Games at 16:00 and 19:00 Thursday.

    """
    total_days = len(day_counter)
    total_times = len(time_counter)
    average_day_count = sum(day_counter.values()) / total_days if total_days > 0 else 0
    average_time_count = (
        sum(time_counter.values()) / total_times if total_times > 0 else 0
    )

    # Check if all times are after 16:00
    all_times_after_1600 = all(time > "16:00" for time in time_counter.keys())

    # Initialize lists to store day and time strings
    day_strings = []
    time_strings = []

    # Iterate over day_counter to construct day strings
    for day, count in day_counter.items():
        if count >= average_day_count:
            day_strings.append(day)
        else:
            day_strings.append(f"occasionally {day}")

    # Iterate over time_counter to construct time strings
    for time, count in time_counter.items():
        if count >= average_time_count:
            time_strings.append(time)
        else:
            time_strings.append(f"occasionally {time}")

    # Join day and time strings with appropriate separators
    day_string = ", ".join(day_strings)
    time_string = ", ".join(time_strings)

    # Add 'evenings' if all times are after 16:00
    if all_times_after_1600:
        day_string += " evenings"

    # Construct the final schedule string
    schedule_string = f"{day_string}. Games at {time_string}"

    return schedule_string


class League(Model):
    __tablename__ = "league"

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, default=datetime.utcnow)
    launch_date = db.Column(db.DateTime, default=datetime.utcnow)
    signup_deadline = db.Column(db.DateTime, default=datetime.utcnow)
    availability_deadline = db.Column(db.DateTime, default=datetime.utcnow)
    schedule_release_date = db.Column(db.DateTime, default=datetime.utcnow)
    bg_color = db.Column(db.String(7), default="#000000")
    fg_color = db.Column(db.String(7), default="#ffffff")

    # Foreign Key for Club with cascading deletes
    club_id = db.Column(db.Integer, db.ForeignKey("club.id", ondelete="CASCADE"))

    # Club Relationship
    club = db.relationship(
        "Club", backref=db.backref("leagues", lazy=True, cascade="all, delete-orphan")
    )

    GDPR_EXPORT_COLUMNS = {}

    def __init__(self, *args, **kwargs):
        """
        This function initiates a new object of class `ModelProxy` and sets up a
        relationship between the new object and an existing `LeagueRules` object
        using the `clubs` attribute.

        """
        super().__init__(*args, **kwargs)
        rules = ModelProxy.clubs.LeagueRules(league=self)
        db.session.add(rules)

    def __repr__(self):
        """
        This function defines a custom `__repr__()` method for the `League` class.

        Returns:
            str: The output returned by the function `__repr__` is:

            `'<League {self.id} - {self.name}>'`.

        """
        return f"<League {self.id} - {self.name}>"

    @transaction
    def add_player_availability(
        self, player, timeslot, availability, add=True, commit=False, force=False
    ):
        """
        Add a player's availability for a specific time slot in the league.

        :param player: The player for whom availability is being updated.
        :param timeslot: The time slot for which availability is being updated.
        :param availability: The availability status (e.g., 0 for unavailable, 1 for available).
        """
        association = self.get_player_association(player)
        # Check if the player is associated with this league
        if force or association:
            # Create or update the PlayerAvailability entry
            player_availability = ModelProxy.clubs.PlayerAvailability.query.filter_by(
                association_id=association.id, timeslot_id=timeslot.id
            ).first()

            if not player_availability:
                player_availability = ModelProxy.clubs.PlayerAvailability(
                    association=association,
                    timeslot=timeslot,
                    availability=availability,
                )
                # print("made new availability for " + player.full_name + " with value " + str(availability))

            else:
                player_availability.availability = availability

            if add:
                db.session.add(player_availability)
            if commit:
                db.session.commit()
        else:
            raise ValueError("Player is not associated with this league.")

    @property
    def players(self):
        """
        This function returns a list of all the players associated with an object
        (presumably a player itself), by iterating over the `player_associations`
        attribute and extracting the `player` element from each `Association` object.

        Returns:
            list: The output returned by this function is a list of all the players
            associated with the `self` object through the `player_associations` attribute.

        """
        return [association.player for association in self.player_associations]

    @property
    def not_players(self):
        # Get the set of players in the current object
        """
        This function returns a list of players that are members of the club but
        not part of the current object's player list.

        Returns:
            list: The output returned by this function is a list of players who
            are members of the club but not part of the current object's players.

        """
        current_players = set(self.players)

        # Get the set of players in the club
        club_players = set(self.club.players)

        # Find players in the club that aren't in the current object's players
        not_in_current = club_players - current_players

        # Convert the result back to a list
        not_in_current_list = list(not_in_current)

        return not_in_current_list

    @transaction
    def get_game_duration(self):
        """
        This function retrieves the duration of the first time slot (ts[0]) from
        a list of TimeSlots and returns it.

        Returns:
            : The function `get_game_duration` returns the duration of the first
            timeslot element inside the `self.timeslots` list.

        """
        ts = self.timeslots[0]
        return ts.get_duration()

    def get_player_availability_object(self, player, timeslot):
        """
        This function retrieves the availability of a player for a specific timeslot
        by checking the player's associations and returning the earliest available
        timeslot or None if no record is found.

        Args:
            player (): The `player` input parameter is used to specify the player
                whose availability is being checked.
            timeslot (): The `timeslot` input parameter specifies the timeslot for
                which the player's availability is being checked.

        Returns:
            None: The output returned by this function is `None`.

        """
        player_association = next(
            (
                assoc
                for assoc in self.player_associations
                if assoc.player_id == player.id
            ),
            None,
        )

        if player_association:
            # Check availability within the player's availability associations
            player_availability = next(
                (
                    avail
                    for avail in player_association.availability_associations
                    if avail.timeslot_id == timeslot.id
                ),
                None,
            )
            if player_availability:
                return player_availability
        # Default to UNK if no availability record found
        return None

    def get_player_availability(self, player, timeslot):
        """
        This function `get_player_availability` takes a `player` and a `timeslot`
        as input and returns the availability of the player during that timeslot.

        Args:
            player (): The `player` input parameter is passed as an argument to
                the `get_player_availability_object()` method inside this function.
            timeslot (dict): The `timeslot` input parameter specifies for which
                time slot the player availability should be checked.

        Returns:
            int: Based on the code provided:

            The output returned by the `get_player_availability` function is a
            single integer value representing the availability of the player for
            the given timeslot.

        """
        player_availability = self.get_player_availability_object(player, timeslot)
        if player_availability:
            return player_availability.availability
        else:
            return -1

    def get_player_availability_dict(self, player):
        """
        This function returns a dictionary of player availability for each timeslot
        (represented by an ID) based on the given player and the availability of
        that player during each timeslot.

        Args:
            player (): The `player` input parameter specifies the player for whom
                to determine availability.

        Returns:
            dict: The function `get_player_availability_dict` returns a dictionary
            with the player availability for each time slot.

        """
        a = {}
        for t in self.timeslots:
            a[t.id] = self.get_player_availability(player, t)
        return a

    def delete_game_event(self, game_event):
        """
        Delete a specific game event from the league.

        :param game_event: The game event to be deleted.
        """
        if game_event in self.game_events:
            self.game_events.remove(game_event)
            db.session.delete(game_event)
            db.session.commit()

    def delete_all_game_events(self):
        """
        Delete all game events associated with the league.
        """
        for game_event in self.game_events:
            db.session.delete(game_event)
        for flight in self.flights:
            flight.report = []
        self.game_events = []
        db.session.commit()

    def log(self):
        """
        The given function `log()` is a method of an object that contains a list
        of flights (`self.flights`). It loops through each flight and prints the
        name of the flight and the player associations for that flight.

        """
        for f in self.flights:
            print(f.name)
            print()
            for fpa in f.player_associations:
                player = fpa.player
                my_string = player.full_name + "\t"
                my_string += str(self.get_player_availability_dict(player))
                print(my_string)
            print()

    def get_player_association(self, player):
        """
        This function `get_player_association` takes a `player` argument and returns
        the associated league for that player from a list of `player_associations`.

        Args:
            player (str): The `player` input parameter specifies the player for
                whom to retrieve the associated league.

        Returns:
            list: The output of this function is `None`.

        """
        league_association = next(
            (
                association
                for association in self.player_associations
                if association.player == player
            ),
            None,
        )
        return league_association

    def create_timeslot(self, start_time, end_time, add=True, commit=False):
        """
        Create a new timeslot associated with this league.

        Args:
            start_time (datetime): The start time of the timeslot.
            end_time (datetime): The end time of the timeslot.

        Returns:
            Timeslot: The newly created Timeslot object.
        """
        new_timeslot = ModelProxy.clubs.Timeslot(
            start_time=start_time,
            end_time=end_time,
            league=self,
        )
        if add is True:
            db.session.add(new_timeslot)

        if commit is True:
            db.session.commit()
        return new_timeslot

    def get_timeslot_by_id(self, id):
        """
        This function takes an ID as input and searches through a list of `Timeslot`
        objects (named `self.timeslots`) to find the one with the matching ID.

        Args:
            id (int): The `id` input parameter specifies the unique identifier of
                the desired `Timeslot` object that should be retrieved from the
                list of `self.timeslots`.

        Returns:
            None: The function "get_timeslot_by_id" returns None if no timeslot
            with the given ID is found.

        """
        for timeslot in self.timeslots:
            if timeslot.id == id:
                return timeslot
        return None

    def get_flight_by_id(self, id):
        """
        The function `get_flight_by_id` takes an ID as input and returns the flight
        with that ID from a list of flights.

        Args:
            id (int): The `id` input parameter is used to retrieve a specific
                flight by its ID.

        Returns:
            None: The output returned by the function `get_flight_by_id` is `None`.

        """
        for f in self.flights:
            if f.id == id:
                return f
        return None

    def create_flight(self, name, add=True, commit=False):
        """
        This function creates a new Flight object and optionally adds it to
        the database (based on the 'add' and 'commit' parameters) and returns
        the created Flight object.

        Args:
            name (str): The `name` parameter specifies the name of the new
                flight being created.
            add (bool): The `add` input parameter is a boolean parameter that
                controls whether or not to add the new `Flight` object to the
                database.
            commit (bool): The `commit` input parameter determines whether to
                immediately commit the changes made to the database after
                creating a new `Flight` object.

        Returns:
            : The output returned by this function is a `ModelProxy` instance
            representing the new flight.

        """
        new_flight = ModelProxy.clubs.Flight(
            name=name,
            league=self,
        )
        if add is True:
            db.session.add(new_flight)

        if commit is True:
            db.session.commit()
        return new_flight

    def add_player(self, player, add=True, commit=False):
        """
        Associate a player with this league.

        :param player: The player to be added to the league.
        """
        association = ModelProxy.clubs.LeaguePlayerAssociation(
            league=self, player=player
        )
        if add is True:
            db.session.add(association)
        if commit is True:
            db.session.commit()

        return association

    def remove_player(self, player, commit=False):
        # Remove player association from the league
        """
        This function removes a player from the league and all its associated
        flights by removing the player's association from the league and each flight.

        Args:
            player (): The `player` input parameter is used to specify the player
                to be removed from the league and all associated flights.
            commit (bool): The `commit` parameter is used to determine whether to
                commit any changes made to the database during the execution of
                the function. If `commit=True`, then any changes made will be
                committed to the database after the function finishes executing.

        """
        league_association = next(
            (
                association
                for association in self.player_associations
                if association.player == player
            ),
            None,
        )
        if league_association:
            self.player_associations.remove(league_association)

        # Remove player association from each flight
        for flight in self.flights:
            self.remove_player_from_flight(player, flight)

        if commit:
            db.session.commit()

    def remove_player_from_flight(self, player, flight):
        """
        This function removes a player from a flight by searching for the player's
        association with the flight and then removing that association if found.

        Args:
            player (): The `player` input parameter specifies the player to be
                removed from the flight.
            flight (): The `flight` input parameter is passed by reference and
                it's the current flight that the player should be removed from.

        """
        flight_association = next(
            (
                association
                for association in flight.player_associations
                if association.player == player
            ),
            None,
        )
        if flight_association:
            flight.player_associations.remove(flight_association)

    def add_facility(self, facility, add=True, commit=False):
        """
        Associate a facility with this league.

        :param facility: The facility to be associated with the league.
        """
        already_in = False
        for facility_assoc in self.facility_associations:
            if facility_assoc.facility.id == facility.id:
                already_in = True
        if already_in is False:
            association = ModelProxy.clubs.LeagueFacilityAssociation(
                league=self, facility=facility
            )
            if add is True:
                db.session.add(association)
            if commit is True:
                db.session.commit()

    def remove_facility_by_id(self, id, commit=False):
        # Find the association with the given facility ID
        """
        This function removes a facility from a collection of facility associations
        based on its ID. If the ID is not found or no facility is associated with
        that ID it returns null.

        Args:
            id (int): The `id` input parameter specifies the ID of the facility
                to be removed from the list of facility associations.
            add (bool): The `add` parameter determines whether or not to add the
                instance of the class (i.e., the self object) to the database if
                the removal of the facility association was successful.
            commit (bool): The `commit` parameter is an optional Boolean value
                that determines whether to commit the changes made to the session
                after removing the facility association.

        """
        facility_to_remove = next(
            (a for a in self.facility_associations if a.facility_id == id), None
        )
        if facility_to_remove:
            self.facility_associations.remove(facility_to_remove)
            if commit:
                db.session.commit()

    def facility_in_league(self, facility):
        """
        This function checks if a given `facility` is present among the facilities
        associated with the object that the function is called on.

        Args:
            facility (): The `facility` input parameter is used to compare against
                the `facility` field of each item included as part of a
                `FacilityAssociation`. The purpose of the `facility` parameter is
                to specify the Facility for which the function will search associated
                FacilityAssociations.

        Returns:
            bool: The function takes an object `self` and a parameter `facility`.

        """
        return any(
            association.facility == facility
            for association in self.facility_associations
        )

    def create_game_event(
        self, players, facility, timeslot, flight, captain=False, add=True, commit=False
    ):
        """
        Create a new game event for the league.

        Args:
            players (list of Player): The list of players associated with the game event.
            facility (Facility): The facility where the game event takes place.
            timeslot (Timeslot): The timeslot when the game event occurs.
            captain (bool): True if one of the players is the captain for this game event, False otherwise.

        Returns:
            LeagueGameEvent: The newly created game event.
        """
        # Check if a game event with the same facility and timeslot already exists
        existing_game_event = self.get_game_event(None, facility, timeslot)
        if existing_game_event:
            return existing_game_event

        if captain is False:
            captain = players[0]

        # Create a new game event
        game_event = ModelProxy.clubs.LeagueGameEvent(
            captain=captain,
            league=self,
            flight=flight,
            facility=facility,
            timeslot=timeslot,
        )

        # Associate players with the game event
        for player in players:
            game_event.players.append(player)

        self.game_events.append(game_event)
        if add is True:
            db.session.add(game_event)
        if commit is True:
            db.session.commit()
        return game_event

    def get_game_event(self, players=None, facility=None, timeslot=None, flight=None):
        """
        Get game events in the league based on optional filters.

        Args:
            players (list of Player): Optional list of players for player-specific game events.
            facility (Facility): Optional filter for facility-specific game events.
            timeslot (Timeslot): Optional filter for timeslot-specific game events.

        Returns:
            list: A list of game events in the league that match the given filters.
        """
        game_events = []

        if players:
            # Filter game events based on any of the specified players
            game_events = [
                ge
                for ge in self.game_events
                if any(player in ge.players for player in players)
            ]

        if facility and not timeslot:
            game_events = [ge for ge in self.game_events if ge.facility == facility]

        if timeslot and not facility:
            game_events = [ge for ge in self.game_events if ge.timeslot == timeslot]

        if facility and timeslot and flight:
            game_events = [
                ge
                for ge in self.game_events
                if ge.facility == facility
                and ge.timeslot == timeslot
                and ge.flight == flight
            ]

        return game_events

    def get_league_rules_dict(self):
        """
        This method returns the league rules associated with this league as a dictionary.

        Returns:
            dict: A dictionary representation of the league rules.
        """
        # Ensure that the league has an associated rules object
        if self.rules:
            return {
                column.name: getattr(self.rules, column.name)
                for column in self.rules.__table__.columns
            }
        else:
            return None
        
    def get_past_player_games(self, player):
        """
        This function retrieves a list of all games that contain a given player
        as an element of the players' list.

        Args:
            player (str): The `player` input parameter is passed as an argument
                to the `get_past_player_games()` function and is used to filter
                which game events should be included inside the resulting list of
                games that are returned by the function.

        Returns:
            list: The function `get_past_player_games` returns a list of games
            called `games`.

        """
        games = []
        for game in self.game_events:
            if player in game.players:
                games.append(game)
        return games


    def clean(self):
        """
        This function 'clean' cleans up the list of facility associations by
        deleting those that have already been seen and adding their facilities to
        a set called 'already_seen'.

        """
        already_seen = set()
        for facility_assoc in self.facility_associations:
            if facility_assoc.facility.id in already_seen:
                db.session.delete(facility_assoc)
            else:
                already_seen.add(facility_assoc.facility.id)

    def get_flight_for_player(self, player):
        """
        Get the flight that contains the specified player.

        Args:
            player (Player): The player for whom to find the containing flight.

        Returns:
            Flight or None: The Flight object containing the player or None if not found.
        """
        for flight in self.flights:
            if flight.player_in_flight(player):
                return flight
        print("fail")
        return None

    def get_start_date(self):
        """
        This function returns the earliest start date of all timeslots associated
        with an instance of the object.

        Returns:
            : The output returned by the function `get_start_date()` is the minimum
            start time of all the timeslots.

        """
        self.start_date = min(self.timeslots, key=lambda ts: ts.start_time).start_time
        return self.start_date

    def get_end_date(self):
        """
        This function returns the end date of a schedule by finding the time slot
        with the earliest start time and returning its start time.

        Returns:
            : The function `get_end_date` returns the maximum start time of all
            `Timeslot` objects within the list `self.timeslots`.

        """
        self.end_date = max(self.timeslots, key=lambda ts: ts.start_time).start_time
        return self.end_date

    def get_launch_date(self):
        """
        The function `get_launch_date` takes the instance object `self` and returns
        the launch date of a product.

        Returns:
            : The output returned by the function `get_launch_date()` is
            `self.start_date - timedelta(days=28)`.

        """
        if self.launch_date is None:
            self.launch_date = self.start_date - timedelta(days=28)
        return self.launch_date

    def get_signup_deadline(self):
        """
        This function calculates and returns the signup deadline based on the start
        date and currently nonexistent signup deadline.

        Returns:
            : The output returned by this function would be `self.start_date - timedelta(days=14)`.

        """
        if self.signup_deadline is None:
            self.signup_deadline = self.start_date - timedelta(days=14)
        return self.signup_deadline

    def get_availability_deadline(self):
        """
        This function sets the availability deadline of an object to 10 days after
        its start date if it is not already set.

        Returns:
            : The output returned by this function is `self.start_date - timedelta(days=10)`.

        """
        if self.availability_deadline is None:
            self.availability_deadline = self.start_date - timedelta(days=10)
        return self.availability_deadline

    def get_schedule_release_date(self):
        """
        This function retrieves the schedule release date based on the start date
        and sets it to 7 days prior if it is not already set.

        Returns:
            : The output returned by this function would be `self.start_date - timedelta(days=7)`.

        """
        if self.schedule_release_date is None:
            self.schedule_release_date = self.start_date - timedelta(days=7)
        return self.schedule_release_date

    def get_days_and_times_string(self):
        """
        This function takes a list of `TimeSlot` objects as input and returns a
        string representing the schedule of these timeslots.

        Returns:
            str: The function "get_days_and_times_string" returns a string
            representing the schedule of slots for a given list of timeslots.

        """
        day_counter = {}
        time_counter = {}
        for ts in self.timeslots:
            day = ts.start_time.strftime("%A")
            time = ts.start_time.strftime("%H:%M")
            if day in day_counter:
                day_counter[day] += 1
            else:
                day_counter[day] = 1
            if time in time_counter:
                time_counter[time] += 1
            else:
                time_counter[time] = 1
        result = construct_schedule_string(day_counter, time_counter)
        return result

    def get_league_description(self):
        """
        The `get_league_description` function returns a string representing a
        simple description of the league.

        Returns:
            str: The output returned by the function `get_league_description()`
            is "A simple description!"

        """
        return "A simple description!"
    
    def is_available_for_signup(self):
        """
        This function checks whether the signup deadline for an object is before
        the current date or not.

        Returns:
            bool: Based on the code provided:
            
            The output returned by this function is `True`.

        """
        today_date = datetime.now()
        signup_date = self.get_signup_deadline()
        return signup_date > today_date
    
    def get_total_flight_issues(self):
        """
        This function returns the total number of flight issues by iterating through
        a list of flights and checking if the "report" key exists in each flight
        object, then adding the value inside the "count" key of that flight report
        to a running total.

        Returns:
            int: The function `get_total_flight_issues` returns the total number
            of issues across all flights in the list of flights passed to it. In
            other words, it returns the sum of the issue counts across all flights.

        """
        i = 0
        for flight in self.flights:
            if flight:
                if flight.report:
                    if 'count' in flight.report:
                        i += flight.report['count']
        return i
    
    def get_ordered_game_events(self):
        # Retrieve the game events associated with the league
        """
        This function retrieves a list of game events associated with a league,
        sorts them based on the start time of each event, and returns the sorted
        list.

        Returns:
            list: The function `get_ordered_game_events` returns a sorted list of
            `GameEvent` objects based on their start time, in descending order.
            In other words, the most recent events are returned first.

        """
        game_events = self.game_events

        # Sort the game events based on the start time
        sorted_game_events = sorted(game_events, key=lambda event: event.timeslot.start_time)

        return sorted_game_events
