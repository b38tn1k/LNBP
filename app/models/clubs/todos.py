from app.models import db, Model

class Todo(Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer(), primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    club_id = db.Column(db.Integer(), db.ForeignKey('club.id'), nullable=False)

    club = db.relationship('Club', back_populates='todos')
