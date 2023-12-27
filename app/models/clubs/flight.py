from app.models import db, Model, ModelProxy

class Flight(Model):
    __tablename__ = 'flight'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # Foreign Key for League
    league_id = db.Column(db.Integer, db.ForeignKey('league.id', ondelete='CASCADE'))

    # Relationship with cascade delete
    league = db.relationship('League', backref=db.backref('flights', lazy=True, cascade='all, delete-orphan'))

    GDPR_EXPORT_COLUMNS = {}

    def __repr__(self):
        """
        This function defines a repr method for a Flight object.

        Returns:
            str: The output returned by this function is:
            
            "<Flight - whatever_name_i_have>"

        """
        return f'<Flight {self.id} - {self.name}>'
    
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
