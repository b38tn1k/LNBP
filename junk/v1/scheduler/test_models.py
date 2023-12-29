from .utils import *
from .gameslots import *
from .player import *
from .single_schedule import *
from .captain_assigner import *
import datetime

def get_recent_monday_midday():
    """
    This function returns the previous Monday at midday (12 PM). If today is Monday
    before 12 PM and today's time is taken into account then the last Monday would
    have been 7 days ago at the same time.

    Returns:
        : The output returned by the function is the current date and time as
        Monday midday (12:00 PM).

    """
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
    """
    This function generates a fake flight schedule for a tennis tournament with
    multiple courts and players. It creates a list of court objects and a list of
    time slot objects representing the schedule for a week (7 days x number of
    days per day), then generates player availability objects based on the time
    slots and adds them to a list of players.

    Args:
        player_count (int): The `player_count` input parameter determines how many
            players will be generated for each team and accordingly assigns
            availability to each player for that day.
        timeslot_count (int): The `timeslot_count` input parameter determines how
            many time slots are generated for each day within the given week count
            and day count.
        court_count (int): The `court_count` input parameter specifies the number
            of courts available for booking.
        day_count (int): The `day_count` input parameter specifies the number of
            days to be included for each week when generating fake flight schedules.
        week_count (int): The `week_count` input parameter specifies the number
            of weeks for which the function should generate fake flights.

    Returns:
        : The function generates a fake flight object with the following attributes:
        
        	- `timeslots`: A list of `TestTimeSlotObj` objects representing the
        available timeslots.
        	- `players`: A list of `TestPlayerObj` objects representing the players
        available for each timeslot.

    """
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
        """
        This function defines a class with an initializer `__init__` that takes
        an `id` parameter and sets the `id` attribute of the object to that value.

        Args:
            id (int): The `id` input parameter is used to set the value of the
                instance attribute `self.id`.

        """
        self.id = id
        self.court_name = random_string(10)

    def get_colliding_events(self, timeslot, id):
        """
        This function returns an empty list (`[]`) of events that collide with the
        specified `timeslot` and `id`.

        Args:
            timeslot (int): The `timeslot` input parameter specifies the time range
                for which the function should search for colliding events.
            id (int): The `id` input parameter is not used anywhere within the
                implementation of the `get_colliding_events()` function.

        Returns:
            list: The output returned by the function `get_colliding_events` with
            the given implementation is an empty list `[]`.

        """
        return []

class TestTimeSlotObj():
    def __init__(self, id, start_time, courts):
        """
        This is a constructor function for an object that initializes its properties:
        	- `id`: sets the object's ID to the input `id`
        	- `start_time`: sets the object's start time to the input `start_time`
        	- `courts`: sets the object's courts to the input `courts`

        Args:
            id (int): The `id` input parameter is used to identify or uniquely
                reference the particular instance of the class being instantiated.
            start_time (str): The `start_time` input parameter specifies the
                starting time of the activity represented by the object being constructed.
            courts (list): The `courts` input parameter is a list of strings
                representing the courts where the matches will be played.

        """
        self.id = id
        self.start_time = start_time
        self.courts = courts

class TestPlayerObj():
    def __init__(self, id):
        """
        This function is a constructor for an object that takes an integer `id`
        and generates a player name using the `random_string` function.

        Args:
            id (int): The `id` input parameter is used to initialise the `self.id`
                attribute of the object with a unique identifier.

        """
        self.id = id
        self.player_name = random_string(10)
        self.availability = []

    def get_availability_obj_for_flight(self, flight_id):
        """
        This function returns the availability object associated with a given
        flight ID.

        Args:
            flight_id (int): The `flight_id` input parameter is used to retrieve
                the availability information for a specific flight.

        Returns:
            : The function `get_availability_obj_for_flight()` returns the
            `availability` object for the given `flight_id`.

        """
        return self.availability
    
    def generate_availability_obj(self, timeslots):
        """
        This function takes a list of `TimeSlot` objects called `timeslots` and
        creates an Availability object from it by adding one availability record
        for each time slot.

        Args:
            timeslots (list): The `timeslots` parameter is a list of objects that
                contain an `id` attribute.

        """
        for ts in timeslots:
            self.availability.append({'timeSlotId': ts.id, 'availability': 1})

class TestFlightObj():
    def __init__(self, timeslots, players):
        """
        This is a special type of Python function called a constructor (also known
        as an initializer or an init method). It takes two arguments `timeslots`
        and `players` and uses them to initialize the object's properties: `events`,
        `timeslots`, and `players`.

        Args:
            timeslots (list): The `timeslots` input parameter specifies a list of
                available time slots for the game.
            players (list): The `players` input parameter is a list of players
                that will be using the scheduling system.

        """
        self.events = []
        self.timeslots = timeslots
        self.players = players
        self.id = 1

    def get_event_objects(self):
        """
        This function returns the list of events associated with the object.

        Returns:
            list: The function `get_event_objects` returns `None`, since `self.events`
            is `undefined`.

        """
        return self.events
    
    def delete_events(self):
        """
        The given function `delete_events` does nothing since it simply contains
        a `pass` statement and no other code.

        """
        pass
