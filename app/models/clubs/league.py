from app.models import db, Model
from datetime import datetime

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
