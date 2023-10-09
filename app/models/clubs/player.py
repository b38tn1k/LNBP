from app.models import Model, db

class Player(Model):
    __tablename__ = 'player'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    contact_number = db.Column(db.String)
    communication_preference_mobile = db.Column(db.Boolean, default=False)
    communication_preference_email = db.Column(db.Boolean, default=False)
    gender = db.Column(db.String)
    club_ranking = db.Column(db.Integer, default=0) # could be inplemented via player ranking

    # Foreign Key for Club with cascading deletes
    club_id = db.Column(db.Integer, db.ForeignKey('club.id', ondelete='CASCADE'))

    # Relationship
    club = db.relationship('Club', backref=db.backref('players', lazy=True, cascade='all, delete-orphan'))

    GDPR_EXPORT_COLUMNS = {
        "id": "ID of the player",
        "hashid": "ID of Player",
        "email": "Player Email",
        "contact_number": "Player Contact Number",
        "communication_preference_mobile": "Player Mobile Communication Preference",
        "communication_preference_email": "Player Email Communication Preference",
        "created": "When the user was created",
        "first_name": "The players first name",
        "last_name": "The players last name",
        "gender": "The player gender",
        "club_ranking": "The player club ranking",
        "email_confirmed": "Whether the email was confirmation"
    }


    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<Player {self.full_name}>'
