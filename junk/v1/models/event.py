from app import db
from . import event_player_association, Model

class Event(Model):
    id = db.Column(db.Integer, primary_key=True)
    timeslot_id = db.Column(db.Integer, db.ForeignKey("timeslot.id"))
    captain_id = db.Column(db.Integer, db.ForeignKey('player.id', name='fk_event_captain_player_id'))
    captain = db.relationship('Player', backref='captained_events')
    players = db.relationship(
        'Player',
        secondary=event_player_association,
        backref=db.backref('events', lazy='dynamic'),
        lazy='dynamic'
    )
    court_id = db.Column(db.Integer, db.ForeignKey('court.id', name='fk_event_court_id'))
    court = db.relationship('Court', backref='events')
    
    def __repr__(self):
        """
        This function defines an `__repr__` method for an object of class `Event`,
        which returns a string representation of the object.

        Returns:
            str: The output returned by this function is:
            
            "<Event **>"

        """
        return f"<Event {self.timeslot.start_time} >"
    
    def get_player_ids(self):
        """
        This function gets all the player IDs from a list of players.

        Returns:
            list: The output returned by this function is an empty list `[]`.

        """
        r = []
        for p in self.players:
            r.append(p.id)
        return r

    
    def get_player_by_id(self, player_id):
        """
        The function `get_player_by_id` takes a `player_id` as an argument and
        returns the first `Player` object with that ID from the list of `Player`
        objects stored by the instance `self`, or `None` if no such player is found.

        Args:
            player_id (int): The `player_id` input parameter specifies which player
                the function should return.

        Returns:
            : The function `get_player_by_id` returns `None` because the iterative
            expression `next((player for playerin self.players if player.id ==
            player_id))` doesn't find any player with the given ID.

        """
        return next((player for player in self.players if player.id == player_id), None)
    
    def update_captain_by_id(self, player_id):
        """
        This function updates the captain of a player with the given player ID by
        using the `get_player_by_id` function to retrieve the player object and
        then updating its `captain` attribute.

        Args:
            player_id (int): The `player_id` input parameter is used to identify
                the specific player that needs to have their captaincy updated.

        """
        p = self.get_player_by_id(player_id)
        self.update_captain(p)

    def update_captain(self, new_captain):
        """
        This function updates the `captain` attribute of an object with the given
        `new_captain` value and commits the change to the database.

        Args:
            new_captain (): The `new_captain` input parameter is used to pass a
                new value for the `captain` attribute of the instance.

        """
        self.captain = new_captain
        db.session.commit()
