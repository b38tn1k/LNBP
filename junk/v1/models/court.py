from app import db
import json
from . import Model


class Court(Model):
    id = db.Column(db.Integer, primary_key=True)
    court_name = db.Column(db.String(64), index=True)
    club_id = db.Column(db.Integer, db.ForeignKey("club.id", name="court_admined_club"))
    club = db.relationship("Club", backref="courts")

    def __repr__(self):
        return "<Court {}>".format(self.court_name)

    def get_timeslots_json(self):
        timeslots_list = []
        for timeslot in self.timeslots:
            timeslot_dict = {
                "id": timeslot.id,
                "title": timeslot.flight.flight_name,
                "start": timeslot.start_time.isoformat(),
                "end": timeslot.end_time.isoformat(),
                "display": "block",
                "backgroundColor": timeslot.flight.bg_color,
                "textColor": timeslot.flight.fg_color,
            }
            timeslots_list.append(timeslot_dict)
        return json.dumps(timeslots_list)

    def get_available(self, timeslot):
        return timeslot in self.timeslots

    def get_colliding_events(self, timeslot, lid):
        collisions = []
        for event in self.events:
            if not event.timeslot:
                db.session.delete(event)
                db.session.commit()
            if lid and event.timeslot:
                if event.timeslot.flight.id != lid:
                    event_start = event.timeslot.start_time
                    event_end = event.timeslot.end_time

                    timeslot_start = timeslot.start_time
                    timeslot_end = timeslot.end_time
                    if (
                        event_start >= timeslot_start and event_start < timeslot_end
                    ) or (event_end >= timeslot_start and event_end < timeslot_end):
                        collisions.append(
                            {
                                "court_id": self.id,
                                "timeslot_id": timeslot.id,
                                "flight_name": event.timeslot.flight.flight_name,
                            }
                        )
        return collisions
