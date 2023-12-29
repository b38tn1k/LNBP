from app import db


class Model(db.Model):
    """ Add a timestamp to all models and allow for serialization."""
    __abstract__ = True

    created = db.Column(db.DateTime(timezone=True),
                        server_default=db.func.now(), nullable=False)
    deleted = db.Column(db.Boolean(), default=False)


flight_player_association = db.Table(
    "flight_player_association",
    db.Column("flight_id", db.Integer, db.ForeignKey("flight.id")),
    db.Column("player_id", db.Integer, db.ForeignKey("player.id")),
)

timeslot_court_association = db.Table(
    "timeslot_court_association",
    db.Column("timeslot_id", db.Integer, db.ForeignKey("timeslot.id")),
    db.Column("court_id", db.Integer, db.ForeignKey("court.id")),
)

event_player_association = db.Table(
    "event_player_association",
    db.Column("event_id", db.Integer, db.ForeignKey("event.id")),
    db.Column("player_id", db.Integer, db.ForeignKey("player.id")),
)
