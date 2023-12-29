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
        return f"<Event {self.timeslot.start_time} >"
    
    def get_player_ids(self):
        r = []
        for p in self.players:
            r.append(p.id)
        return r

    
    def get_player_by_id(self, player_id):
        return next((player for player in self.players if player.id == player_id), None)
    
    def update_captain_by_id(self, player_id):
        p = self.get_player_by_id(player_id)
        self.update_captain(p)

    def update_captain(self, new_captain):
        self.captain = new_captain
        db.session.commit()
