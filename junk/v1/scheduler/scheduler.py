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
    for new in sublist:
        new.runCA()
        new.recalculate_players()
        new.recalculate_players()


def summarise_all_candidates(sublist):
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
    g_candidates = []
    for new in a_candidates:
        if (new.check_escape_conditions()):
            g_candidates.append(new)
    return g_candidates


def find_best_candidate(g_candidates):
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
    print("Result")
    for key in rs:
        print(key, rs[key])
    
    print("\nPool Stats")
    for key in metrics:
        print(key, metrics[key], ":", i)


class Scheduler:
    def __init__(self, flight):
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
        print('assign captains')
        ca = CaptainAssigner(self.flight_obj)
        res = ca.run()
        return res

    def testMode(self, player_count, timeslot_count, court_count, day_count, week_count, iterations):
        self.test = True
        self.player_count = player_count
        self.flight_obj = generateFakeFlight(player_count, timeslot_count, court_count, day_count, week_count)
        self.iterations = iterations
        # print(player_count, timeslot_count, court_count, day_count, week_count)

    def write_to_database(self, bc):
        if not self.test:
            bc.create_events()

    def setup_generate(self):
        self.flight_obj.delete_events()
        template, gameslots = findAllGameSlots(self.flight_obj, self.rules)
        self.g_candidates = []
        self.a_candidates = []
        for _ in range(self.iterations):
            self.a_candidates.append(SingleSchedule(self.flight_obj, template, copy_gameslots(gameslots)))

    def complete_generate(self):
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
        self.setup_generate()
        
        process_candidates(self.a_candidates)
        
        res = self.complete_generate()
        return res
