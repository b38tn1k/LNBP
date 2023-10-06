from app.models import db, Model
from datetime import datetime
from .player_availability import PlayerAvailability
from .league_game_event import LeagueGameEvent

class League(Model):
    __tablename__ = 'league'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    bg_color = db.Column(db.String(7), default='#000000')
    fg_color = db.Column(db.String(7), default='#ffffff')

    # Foreign Key for Club with cascading deletes
    club_id = db.Column(db.Integer, db.ForeignKey('club.id', ondelete='CASCADE'))

    # Club Relationship
    club = db.relationship('Club', backref=db.backref('leagues', lazy=True, cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<League {self.id} - {self.name}>'
    
    def add_player_availability(self, player, timeslot, availability):
        """
        Add a player's availability for a specific time slot in the league.

        :param player: The player for whom availability is being updated.
        :param timeslot: The time slot for which availability is being updated.
        :param availability: The availability status (e.g., 0 for unavailable, 1 for available).
        """
        # Check if the player is associated with this league
        if player in self.players:
            # Create or update the PlayerAvailability entry
            player_availability = PlayerAvailability.query.filter_by(player=player, timeslot=timeslot).first()
            if not player_availability:
                player_availability = PlayerAvailability(player=player, timeslot=timeslot, availability=availability)
            else:
                player_availability.availability = availability
            db.session.add(player_availability)
            db.session.commit()
        else:
            raise ValueError("Player is not associated with this league.")
        
    def get_player_availability(self, player, timeslot):
        """
        Get a player's availability for a specific time slot in the league.

        :param player: The player for whom availability is requested.
        :param timeslot: The time slot for which availability is requested.
        :return: The availability status (e.g., 0 for unavailable, 1 for available).
        """
        player_availability = PlayerAvailability.query.filter_by(player=player, timeslot=timeslot).first()
        if player_availability:
            return player_availability.availability
        else:
            # Default to unavailable if no availability record found
            return 0
        
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
            new_game_event = LeagueGameEvent(player=player, facility=facility, timeslot=timeslot)
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




