from app import db
from . import timeslot_court_association, Model
from .event import Event


class Timeslot(Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey("flight.id"))
    events = db.relationship("Event", backref="timeslot")
    # Many-to-many relationship with Court
    courts = db.relationship(
        'Court',
        secondary=timeslot_court_association,
        backref=db.backref('timeslots', lazy='dynamic'),
        lazy='dynamic'
    )

    def get_event_for_court_id(self, court_id):
        return next((event for event in self.events if event.court_id == court_id), None)

    def __repr__(self):
        return f"<Timeslot {self.start_time} - {self.end_time}>"
    
    def get_human_readable_date(self):
        # Format the start_time into a human-readable date string
        day_name = self.start_time.strftime("%A")  # Get the full day name (e.g., Monday)
        date_month = self.start_time.strftime("%B %d")  # Get the date and month (e.g., 25 July)
        time = self.start_time.strftime("%I:%M %p")  # Get the time in HH:MM AM/PM format
        return f"{day_name} {date_month}<br>{time}"
    
    def get_human_readable_day_number_month_year(self):
        return self.start_time.strftime("%A %m/%d/%Y")
    
    def get_human_readable_date_time_short(self):
        # Format the start_time into a human-readable date string
        day_name = self.start_time.strftime("%A")  # Get the full day name (e.g., Monday)
        # date_month = self.start_time.strftime("%d/%m")  # Get the date and month (e.g., 25 July)
        date_month = self.start_time.strftime("%m/%d")  # Get the date and month (e.g., 25 July)
        time = self.start_time.strftime("%I:%M")  # Get the time in HH:MM AM/PM format
        return f"{day_name[0:3]}<br>{date_month}<br>{time}"
    
    def get_human_readable_date_day_month(self):
        # Format the start_time into a human-readable date string
        # day_name = self.start_time.strftime("%A")  # Get the full day name (e.g., Monday)
        # date_month = self.start_time.strftime("%B %d")  # Get the date and month (e.g., 25 July)
        date_month = self.start_time.strftime("%m/%d")  # Get the date and month (e.g., 25 July)
        return date_month#f"{day_name} {date_month}"
    
    def get_human_readable_time(self):
        time = self.start_time.strftime("%I:%M")  # Get the time in HH:MM AM/PM format
        return time
    
    def get_events(self): 
        a = []
        for e in self.events:
            if e.court:
                res = {}
                res['flight'] = self.flight_id
                res['flight_name'] = self.flight.flight_name
                res['timeslot'] = self.id
                res['readable_date'] = self.get_human_readable_day_number_month_year()
                res['readable_time'] = self.get_human_readable_time()
                res['datetime_obj'] = self.start_time
                res['court'] = e.court_id
                res['court_name'] = e.court.court_name
                res['players'] = []
                res['player_names'] = []
                res['captain'] = -1
                res['captain_name'] = "None"
                if e.captain:
                    res['captain'] = e.captain.id
                    res['captain_name'] = e.captain.player_name
                else:
                    res['captain'] = 34
                for p in e.players:
                    res['player_names'].append(p.player_name)
                    res['players'].append(p.id)
                a.append(res)
        return a
    
    def get_event_objects(self): 
        a = []
        for e in self.events:
            a.append(e)
        return a
    

    def delete_event_with_court_id(self, court_id):
        for e in self.events:
            if e.court_id == court_id:
                db.session.delete(e)
                #break
        db.session.commit()
        return True
    
    def get_court_by_id(self, court_id):
        return self.courts.filter_by(id=court_id).first()
    
    def delete_all_events(self, commit):
        for e in self.events:
            db.session.delete(e)
        if commit:
            db.session.commit()

    def on_delete(self):
        self.delete_all_events(False)
    
    def create_event(self, court, players, captain=None):
        # Filter existing events using Python's built-in filter function
        matching_events = list(filter(
            lambda e: e.court == court and e.captain == captain, 
            self.events
        ))

        # Find the first event with matching players, if any
        existing_event = None
        for event in matching_events:
            existing_player_ids = {player.id for player in event.players}
            new_player_ids = {player.id for player in players}
            if existing_player_ids == new_player_ids:
                existing_event = event
                break

        # If a matching event is found, return its ID
        if existing_event:
            return existing_event.id

        # If no matching event is found, create a new one
        event = Event(timeslot=self, court=court, captain=captain)
        for player in players:
            event.players.append(player)
        
        db.session.add(event)
        db.session.commit()
        return event.id
