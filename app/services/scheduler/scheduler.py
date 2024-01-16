from .single_flight_scheduler_tool import SingleFlightScheduleTool
from .constants import *

def generateGameSlotAvailabilityScores(gameslots, players):
    """
    This function generates the availability score for each game slot (gs) based
    on the availability of players (p) during that timeslot.

    Args:
        gameslots (list): The `gameslots` input parameter is a list of game slots.
        players (list): The `players` input parameter is a list of player objects
            that the function iterates over to determine their availability for
            each game slot.

    """
    for gs in gameslots:
        for p in players:
            if p.availability[gs.timeslot_id] == AVAILABLE:
                gs.availability_score += p.availability_score
    print ([g.availability_score for g in gameslots])

            