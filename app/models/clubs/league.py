from app.models import db, Model
from datetime import datetime
from app.models import ModelProxy, transaction

class League(Model):
    __tablename__ = 'league'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, default=datetime.utcnow)
    bg_color = db.Column(db.String(7), default='#000000')
    fg_color = db.Column(db.String(7), default='#ffffff')

    # Foreign Key for Club with cascading deletes
    club_id = db.Column(db.Integer, db.ForeignKey('club.id', ondelete='CASCADE'))

    # Club Relationship
    club = db.relationship('Club', backref=db.backref('leagues', lazy=True, cascade='all, delete-orphan'))

    GDPR_EXPORT_COLUMNS = {}

    def __repr__(self):
        """
        This function defines a custom `__repr__()` method for the `League` class.

        Returns:
            str: The output returned by the function `__repr__` is:
            
            `'<League {self.id} - {self.name}>'`.

        """
        return f'<League {self.id} - {self.name}>'
    
    @transaction
    def add_player_availability(self, player, timeslot, availability, add=True, commit=False, force=False):
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
                association_id=player.id, timeslot_id=timeslot.id).first()

            if not player_availability:
                player_availability = ModelProxy.clubs.PlayerAvailability(
                    association_id=player.id, timeslot_id=timeslot.id, availability=availability)

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


    def get_player_availability(self, player, timeslot):
        """
        Get a player's availability for a specific time slot in the league.

        :param player: The player for whom availability is requested.
        :param timeslot: The time slot for which availability is requested.
        :return: The availability status (e.g., 0 for unavailable, 1 for available).
        """
        # Using self.player_associations to directly access the relevant associations
        player_association = next((assoc for assoc in self.player_associations if assoc.player_id == player.id), None)

        if player_association:
            # Check availability within the player's availability associations
            player_availability = next((avail for avail in player_association.availability_associations if avail.timeslot_id == timeslot.id), None)
            if player_availability:
                return player_availability.availability
        # Default to unavailable if no availability record found
        return 0
    
    @transaction
    def get_existing_game_event(self, player, facility, timeslot):
            """
            Get an existing game event that matches the specified player, facility, and timeslot.

            :param player: The player associated with the game event.
            :param facility: The facility associated with the game event.
            :param timeslot: The timeslot associated with the game event.
            :return: The existing game event or None if not found.
            """
            for game_event in self.game_events:
                if (
                    game_event.player == player
                    and game_event.facility == facility
                    and game_event.timeslot == timeslot
                ):
                    return game_event
            return None
    
    @transaction
    def add_game_event(self, player, facility, timeslot):
        """
        Add a new game event to the league if one with the same player, facility, and timeslot doesn't already exist.

        Parameters:
        - player (Player): The player associated with the game event.
        - facility (Facility): The facility associated with the game event.
        - timeslot (Timeslot): The timeslot associated with the game event.

        Returns:
        - LeagueGameEvent: The newly created or existing game event.
        """
        # Check if a game event with the specified player, facility, and timeslot exists
        existing_game_event = self.get_existing_game_event(player, facility, timeslot)

        if existing_game_event:
            # An existing game event was found, so we won't add a new one
            return existing_game_event
        else:
            # Create and add a new game event
            new_game_event = ModelProxy.clubs.LeagueGameEvent(player=player, facility=facility, timeslot=timeslot)
            self.game_events.append(new_game_event)
            db.session.add(new_game_event)
            db.session.commit()
            return new_game_event

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
                name = name,
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
        # Create a new association between the flight and the player
        association = ModelProxy.clubs.LeaguePlayerAssociation(league=self, player=player)
        if add is True:
            db.session.add(association)
        if commit is True:
            db.session.commit()
        return association




