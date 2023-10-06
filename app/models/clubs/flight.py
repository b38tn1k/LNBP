from app.models import db, Model

class Flight(Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # Foreign Key for League
    league_id = db.Column(db.Integer, db.ForeignKey('league.id', ondelete='CASCADE'))

    # Relationship with cascade delete
    league = db.relationship('League', backref=db.backref('flights', lazy=True, cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<Flight {self.id} - {self.name}>'
