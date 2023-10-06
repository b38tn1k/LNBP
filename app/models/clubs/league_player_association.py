from app.models import db, Model

class LeaguePlayerAssociation(Model):
    __tablename__ = 'league_player_association'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign keys for League and Player with cascading deletes
    league_id = db.Column(db.Integer, db.ForeignKey('league.id', ondelete='CASCADE'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id', ondelete='CASCADE'))

    # Relationships
    league = db.relationship('League', backref=db.backref('player_associations', lazy=True, cascade='all, delete-orphan'))
    player = db.relationship('Player', backref=db.backref('league_associations', lazy=True, cascade='all, delete-orphan'))
