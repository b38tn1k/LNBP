from .utils import *
from .gameslots import *
from .player import *
from .single_schedule import *
from .captain_assigner import *
import datetime

def get_recent_monday_midday():
    now = datetime.datetime.now()
    
    # if today is Monday but before midday
    if now.weekday() == 0 and now.hour < 12:
        last_monday = now - datetime.timedelta(days=7)
        return last_monday.replace(hour=12, minute=0, second=0, microsecond=0)
    
    # if today is Monday and time is 12 PM or later, or if it's any other day
    delta_days = now.weekday() # 0 = Monday, 1 = Tuesday, ...
    last_monday = now - datetime.timedelta(days=delta_days)
    return last_monday.replace(hour=12, minute=0, second=0, microsecond=0)

def generateFakeFlight(player_count, timeslot_count, court_count, day_count, week_count):
    flight_obj = None
    courts = []
    for i in range(court_count):
        courts.append(TestCourtObj(i))

    timeslots = []
    start_date = get_recent_monday_midday()
    for i in range(week_count):
        for j in range(day_count):
            for k in range(timeslot_count):
                new_date = start_date + datetime.timedelta(days=(7 * i + j), hours = k)
                timeslots.append(TestTimeSlotObj(len(timeslots), new_date, courts))

    players = []
    for i in range(player_count):
        p = TestPlayerObj(i)
        p.generate_availability_obj(timeslots)
        players.append(p)

    flight = TestFlightObj(timeslots, players)
    return flight


class TestCourtObj():
    def __init__(self, id):
        self.id = id
        self.court_name = random_string(10)

    def get_colliding_events(self, timeslot, id):
        return []

class TestTimeSlotObj():
    def __init__(self, id, start_time, courts):
        self.id = id
        self.start_time = start_time
        self.courts = courts

class TestPlayerObj():
    def __init__(self, id):
        self.id = id
        self.player_name = random_string(10)
        self.availability = []

    def get_availability_obj_for_flight(self, flight_id):
        return self.availability
    
    def generate_availability_obj(self, timeslots):
        for ts in timeslots:
            self.availability.append({'timeSlotId': ts.id, 'availability': 1})

class TestFlightObj():
    def __init__(self, timeslots, players):
        self.events = []
        self.timeslots = timeslots
        self.players = players
        self.id = 1

    def get_event_objects(self):
        return self.events
    
    def delete_events(self):
        pass
