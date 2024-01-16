from .single_flight_scheduler_tool import SingleFlightScheduleTool
from .constants import *

def generateGameSlotAvailabilityScores(gameslots, players):
    for gs in gameslots:
        for p in players:
            if p.availability[gs.timeslot_id] == AVAILABLE:
                gs.availability_score += p.availability_score
        print(gs, gs.availability_score)

            