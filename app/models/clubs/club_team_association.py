from app.models import db, Model

class ClubTeamAssociation(Model):
    __tablename__ = 'club_team_association'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)

    # Foreign keys for Club and Team
    club_id = db.Column(db.Integer, db.ForeignKey('club.id', ondelete='CASCADE'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id', ondelete='CASCADE'))

    # Relationships
    club = db.relationship('Club', backref=db.backref('team_associations', lazy=True, cascade='all, delete-orphan'))
    team = db.relationship('Team', backref=db.backref('club_associations', lazy=True, cascade='all, delete-orphan'))

    @staticmethod
    def create(club_id, team_id):
        association = ClubTeamAssociation(club_id=club_id, team_id=team_id)
        db.session.add(association)
        db.session.commit()
        return association
