#TODO: white label player facing portals for Clib header / colors / fonts / etc
#TODO: cn pul from other pools at the same timeslot sometimes (choose flights)
#TODO: double header field, week gap field, visual indication for double header in the grid
#TODO: max double headers
#TODO: Full calendar to outlook and google calendar
#TODO: Twilio integration
# display 'leftovers' for each gameslot
#WORST CASE: 4 flights of 12,4 time slots, 5 courts
# TODO: https://blakestevenson.github.io/utr-api-docs/
#TODO: generate score cards CSVs thing from google drive Wills thing
#TODO rule breaking UIs

from app import db
import pytz
from datetime import datetime, timedelta
from random import shuffle, choice, seed
import time
import math
from .utils import *
from .gameslots import *
from .player import *
from .single_schedule import *
from .captain_assigner import *
from .test_models import *


# be sub-aware, if there are 12 people in the flight, schedule 8 max
# make warning flag on the front end draggable-item source

def process_candidates(sublist):
    """
    This function processes each candidate (sublist element) by running their
    `runCA()` method and recalculating players and player information using the
    result of that method.

    Args:
        sublist (list): The `sublist` input parameter is a list of objects (e.g.,
            players), and the function processes each object In the list by calling
            methods `runCA()` and `recalculate_players()` on each object.

    """
    for new in sublist:
        new.runCA()
        new.recalculate_players()
        new.recalculate_players()


def summarise_all_candidates(sublist):
    """
    This function takes a list of candidates and aggregates the results of their
    `summarise_tests()` method calls to produce a dictionary of test metrics. It
    recursively iterates over the sublists of candidates and adds the values of
    each key found by the previous iteration to the current value of the same key
    or initializes a new key-value pair if it doesn't exist yet.

    Args:
        sublist (list): The `sublist` parameter is a list of candidates that should
            be processed by the function.

    Returns:
        dict: The output returned by this function is a dictionary of summarized
        test results for all candidatesin the sublist.

    """
    metrics = {}
    for c in sublist:
        r = c.summarise_tests()
        for k in r:
            if k in metrics:
                metrics[k] += r[k]
            else:
                metrics[k] = r[k]
    return metrics


def find_good_candidates(a_candidates):
    """
    This function takes an iterable `a_candidates` and returns a new list
    `g_candidates` containing only the candidates that pass the `check_escape_conditions()`
    method.

    Args:
        a_candidates (list): The `a_candidates` input parameter is a list of
            candidates that will be iterated over and filtered to find good
            candidates based on the `check_escape_conditions()` method.

    Returns:
        list: The output returned by this function is an empty list `[]`, because
        the loop does not find any candidates that pass the `check_escape_conditions()`
        method.

    """
    g_candidates = []
    for new in a_candidates:
        if (new.check_escape_conditions()):
            g_candidates.append(new)
    return g_candidates


def find_best_candidate(g_candidates):
    """
    This function `find_best_candidate` takes a list of game candidates and returns
    the best candidate based on their average and maximum player luck. It does
    this by iterating through the list of candidates and comparing their luck
    metrics to the current leader's metrics. If a new candidate has a better maximum
    luck or lower variance than the current leader and its average luck is within
    a certain range of the current leader's average luck and the maximum luck of
    all candidates is the highest of any of them.

    Args:
        g_candidates (list): The `g_candidates` input parameter is a list of objects
            that contain the average and max player luck information for each candidate.

    Returns:
        : The output returned by the `find_best_candidate` function is `g_candidates[0]`.

    """
    result = g_candidates[0].get_average_and_max_player_luck()
    leader = [g_candidates[0], result]
    bc = leader[0]
    min_max_common = leader[1]["max"]
    for c in g_candidates:
        result = c.get_average_and_max_player_luck()
        if (
            result["max"] <= min_max_common
            and result["variance"] <= leader[1]["variance"]
            and result["average"] <= leader[1]["average"]
        ):
            leader = [c, result]
            min_max_common = result["max"]
            bc = leader[0]
    return bc


def log_res(rs, metrics, i):
    """
    The function `log_res` prints the contents of two dictionaries: `rs` and `metrics`.

    Args:
        rs (dict): The `rs` input parameter is a dictionary that contains the
            results of the API calls.
        metrics (dict): The `metrics` input parameter is a dictionary that contains
            various statistics (e.g.
        i (int): The `i` input parameter is not used within the body of the
            `log_res()` function.

    """
    print("Result")
    for key in rs:
        print(key, rs[key])
    
    print("\nPool Stats")
    for key in metrics:
        print(key, metrics[key], ":", i)


class Scheduler:
    def __init__(self, flight):
        """
        This function sets up a Flight simulator and prepares it to play a game
        with a specific flight.

        Args:
            flight (): The `flight` input parameter is used to pass an instance
                of the `Flight` class to the `__init__` method.

        """
        seed(int(datetime.datetime.now().timestamp()))
        self.test = False
        self.flight_obj = flight
        self.flight_name = flight.flight_name
        self.rules = tempRules
        self.player_count = 0
        if flight:
            for player in flight.players: # can't len a database
                self.player_count += 1
            self.iterations = round(POOL_ITERATIONS / self.player_count) + 1

    def assign_captains(self):
        """
        This function "assign_captains" defines aCaptainAssigner object (called
        "ca") and calls the "run" method of that object.

        Returns:
            : Based on the code provided:
            
            The output returned by this function is:
            
            "assign captains".

        """
        print('assign captains')
        ca = CaptainAssigner(self.flight_obj)
        res = ca.run()
        return res

    def testMode(self, player_count, timeslot_count, court_count, day_count, week_count, iterations):
        """
        This function sets a test mode for an object and sets various parameters
        such as player count and iteration count for testing purposes.

        Args:
            player_count (int): The `player_count` input parameter determines the
                number of players for which flights will be generated.
            timeslot_count (int): Based on the code provided:
                
                The `timeslot_count` input parameter sets the number of timeslots
                for each flight.
            court_count (int): Based on the given code snippet and function
                documentation comments:
                
                The `court_count` input parameter sets the number of courts used
                for testing purposes.
            day_count (int): The `day_count` input parameter specifies the number
                of days for which the fake flight schedule should be generated.
            week_count (int): Based on the code snippet provided:
                
                The `week_count` parameter specifies the number of weeks to generate
                flights for.
            iterations (int): The `iterations` input parameter specifies the number
                of times the `testMode` function should run the simulation.

        """
        self.test = True
        self.player_count = player_count
        self.flight_obj = generateFakeFlight(player_count, timeslot_count, court_count, day_count, week_count)
        self.iterations = iterations
        # print(player_count, timeslot_count, court_count, day_count, week_count)

    def write_to_database(self, bc):
        """
        This function calls the `create_events()` method of an object referred to
        by `bc`, but only if a certain flag (`test`) is not set to `True`.

        Args:
            bc (): The `bc` parameter is an instance of the `BaseClass` class and
                it contains the methods that are needed to create events for the
                `TestClass` instance being processed.

        """
        if not self.test:
            bc.create_events()

    def setup_generate(self):
        """
        This function clears the events of the `flight_obj`, finds all game slots
        and candidate solutions for a given set of rules using the `findAllGameSlots()`
        function and the `SingleSchedule()` constructor.

        """
        self.flight_obj.delete_events()
        template, gameslots = findAllGameSlots(self.flight_obj, self.rules)
        self.g_candidates = []
        self.a_candidates = []
        for _ in range(self.iterations):
            self.a_candidates.append(SingleSchedule(self.flight_obj, template, copy_gameslots(gameslots)))

    def complete_generate(self):
        """
        This function "complete_generate" takes a pool of candidate solutions and
        generates the best solution by performing various steps:
        1/ Summarizes all candidates.
        2/ Finds the best candidate based on failure count.
        3/ Checks escape conditions for the best candidate.
        4/ Writes the best candidate to a database.
        5/ Reports the results including the best candidate's statistics and pool
        statistics.
        The function returns a dictionary containing the selected statistics and
        pool statistics.

        Returns:
            dict: The function returns a dictionary with two key-value pairs:
            
            	- {'selected_stats': <summarized test results>, 'pool_stats': <candidate
            pool metrics>}

        """
        metrics = {}
        metrics = summarise_all_candidates(self.a_candidates)
        
        self.g_candidates = find_good_candidates(self.a_candidates)

        if len(self.g_candidates) == 0:
            self.g_candidates = self.a_candidates
            bc = min(self.a_candidates, key=lambda c: c.get_average_failure_count())
        else:
            bc = find_best_candidate(self.g_candidates)
                
        bc.check_escape_conditions(True)
        self.write_to_database(bc)
        rs = bc.summarise_tests()
        # timer_report()
        log_res(rs, metrics, self.iterations)

        return ({'selected_stats': rs, 'pool_stats': metrics})

    def generate(self):
        """
        This function is undefined. It does not contain any code or a specific purpose.

        Returns:
            : The output returned by this function is `None`, as there is no
            explicit `return` statement at the end of the function.

        """
        self.setup_generate()
        
        process_candidates(self.a_candidates)
        
        res = self.complete_generate()
        return res
