from app.models import db, Model, ModelProxy
from sqlalchemy.dialects.postgresql import ARRAY

class Flight(Model):
    __tablename__ = 'flight'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # Foreign Key for League
    league_id = db.Column(db.Integer, db.ForeignKey('league.id', ondelete='CASCADE'))

    # Relationship with cascade delete
    league = db.relationship('League', backref=db.backref('flights', lazy=True, cascade='all, delete-orphan'))
    # report = db.Column(db.JSON, default=lambda: []) 
    report = db.Column(db.JSON) # untested

    GDPR_EXPORT_COLUMNS = {}

    def __repr__(self):
        """
        This function defines a repr method for a Flight object.

        Returns:
            str: The output returned by this function is:
            
            "<Flight - whatever_name_i_have>"

        """
        return f'<Flight ID {self.id} - {self.name}>'
    
    def add_player(self, player, add=True, commit=False):
        """
        Associate a player with this flight.

        :param player: The player to be added to the flight.
        """
        # Create a new association between the flight and the player
        association = ModelProxy.clubs.FlightPlayerAssociation(flight=self, player=player)
        if add is True:
            db.session.add(association)
        if commit is True:
            db.session.commit()
        return association
    
    def player_in_flight(self, player):
        """
        This function checks whether a given `player` is associated with the
        `PlayerManager` object. It does this by iterating through the list of
        `player associations` stored on the `PlayerManager` and checking if any
        of them match the given `player`. If such an association is found (i.e.,
        one of the associations has the same `player` as the argument passed to
        the function), the function returns `True`, indicating that the player is
        associated with the `PlayerManager`.

        Args:
            player (): The `player` input parameter is passed to the function and
                is used within the loop to compare it with the `player` attribute
                of each associated entity.

        Returns:
            bool: The output returned by this function is `False`.

        """
        for ass in self.player_associations:
            if ass.player == player:
                return True
        return False
    
    def delete_all_game_events(self):
        """
        Delete all game events associated with the league.
        """
        self.report = {'count':0}
        for game_event in self.game_events:
            db.session.delete(game_event)
        self.game_events = []
        db.session.commit()
