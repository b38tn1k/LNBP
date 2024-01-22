from app.models import db, Model
from datetime import datetime
from app.models import ModelProxy, transaction


class League(Model):
    __tablename__ = "league"

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, default=datetime.utcnow)
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
        # Check if the player is associated with this league
        if force or self.player_associations.filter_by(player_id=player.id).first():
            # Create or update the PlayerAvailability entry
            player_availability = ModelProxy.clubs.PlayerAvailability.query.filter_by(
                association_id=player.id, timeslot_id=timeslot.id
            ).first()

            if not player_availability:
                player_availability = ModelProxy.clubs.PlayerAvailability(
                    association_id=player.id,
                    timeslot_id=timeslot.id,
                    availability=availability,
                )

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
        self.game_events = []
        db.session.commit()

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
        
    def clean(self):
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
