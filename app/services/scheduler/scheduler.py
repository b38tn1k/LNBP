from .single_flight_scheduler_tool import SingleFlightScheduleTool
from .constants import *
from .player import Player
from .gameslot import GameSlot


class Scheduler:
    SINGLE_FLIGHT = 0

    def __init__(self, league, mode, flight_id=None):
        """
        This function defines a class's constructor and sets some of its attributes
        and method pointers based on the value of the "mode" argument passed to
        the constructor.

        Args:
            league (dict): The `league` input parameter is used to set the current
                league being played.
            mode (int): The `mode` input parameter specifies the type of flights
                to be executed.
            flight_id (str): The `flight_id` input parameter specifies which
                particular flight the object should be configured for.

        """
        self.league = league
        self.rules = league.get_league_rules_dict()
        self.flight_id = flight_id
        self.scheduler = None

        if mode == self.SINGLE_FLIGHT or mode == self.ALL_FLIGHTS:
            self.prepare = self.sf_prepare
            self.setup = self.sf_setup
            self.build = self.sf_build

    def sf_prepare(self):
        """
        This function prepares a flight object for use by deleting all game events
        associated with it.

        """
        self.flight = self.league.get_flight_by_id(self.flight_id)
        self.flight.delete_all_game_events()

    def sf_setup(self, mutate):
        """
        This function creates a scheduling tool (a `SingleFlightScheduleTool`) for
        a fantasy football league using the given flight data and rules.

        Args:
            mutate (bool): The `mutate` parameter is used to determine whether the
                created schedule should be modified to intentionally introduce
                bias into the matchups.

        Returns:
            : The function returns a `SingleFlightScheduleTool` object.

        """
        players = create_player_objects(self.flight, self.league, self.rules)
        gameslots = create_gameslot_objects(self.league, self.rules)
        generateGameSlotAvailabilityScores(gameslots, players)
        scheduler = SingleFlightScheduleTool(
            self.flight.id, self.rules, players, gameslots, mutate
        )
        return scheduler

    def sf_build(self, scheduler):
        """
        This function takes a scheduler and iterates through its returned events
        (i.e., games) and creates a game for each one using the `create_game_from_scheduler`
        function.

        Args:
            scheduler (): The `scheduler` input parameter is passed as an iterable
                of events that should be used to create games using the
                `create_game_from_scheduler` method.

        """
        for e in scheduler.return_events():
            create_game_from_scheduler(self.league, e, flight=self.flight)

    def evaluate(self, scheduler):
        """
        This function evaluates the given scheduler's compliance with two tiers
        of rules. It returns a dictionary of rule violations (i.e., "fails")
        counting the number of times each rule was broken.

        Args:
            scheduler (dict): The `scheduler` input parameter is a Python scheduler
                object that contains information about which players have satisfied
                their roles and when.

        Returns:
            dict: The output returned by this function is a dictionary with two
            keys: "tier1" and "tier2".

        """
        player_check = summarize_schedule(scheduler)
        fails = {"tier1": 0, "tier2": 0}  # rules broken counter

        for player in player_check:
            p = player_check[player]
            # print(p)
            # print()
            # player satisfied
            fails["tier1"] += int(not p["satisfied"])
            # captainship
            captainhood_ok = (
                p["captain_count"] <= p["rules"]["max_captained"]
                and p["captain_count"] >= p["rules"]["min_captained"]
            )
            fails["tier2"] += not captainhood_ok

        return fails

    def run(self):
        """
        This function is a candidate scheduler for an undeteremined Python class
        `League`. It iterates over the timeslots of the league and finds the best
        scheduling plan based on two tiers of evaluation metrics.

        """
        self.prepare()
        i = 0
        candidates = []
        for _ in self.league.timeslots:
            for _ in range(2):
                scheduler = self.setup(i)
                i += 1
                scheduler.run()
                res = self.evaluate(scheduler)
                candidates.append({"scheduler": scheduler, "res": res})
        best_candidate = min(candidates, key=lambda x: (x['res']['tier1'], x['res']['tier2']))
        print(best_candidate)
        self.build(best_candidate['scheduler'])


def summarize_schedule(scheduler):
    """
    This function takes a schedule (a list of game slots and their players) and
    returns a dictionary of each player's availability across different days and
    weeks. It calculates the number of games each player is available for and
    records any collisions between players (i.e.

    Args:
        scheduler (dict): The `scheduler` input parameter is used to pass the
            schedule data for which the function should calculate the availability
            and collisions of players for each game slot.

    Returns:
        dict: The function `summarize_schedule` returns a dictionary of player checks.

    """
    player_check = {}
    for player in scheduler.players:
        player_check[player.id] = {
            "collisions": {},
            "captain_count": player.captain_count,
            "satisfied": player.satisfied,
            "rules": player.rules,
            "day_numbers": {},
            "week_numbers": {},
            AVAILABLE: 0,
            AVAILABLE_LP: 0,
            UNAVAILABLE: 0,
        }

    for event in scheduler.gameslots:
        for p in event.game_event:
            player_check[p.id][p.availability[event.timeslot_id]] += 1
            if event.day_number in player_check[p.id]["day_numbers"]:
                player_check[p.id]["day_numbers"][event.day_number] += 1
            else:
                player_check[p.id]["day_numbers"][event.day_number] = 1
            if event.week_number in player_check[p.id]["week_numbers"]:
                player_check[p.id]["week_numbers"][event.week_number] += 1
            else:
                player_check[p.id]["week_numbers"][event.week_number] = 1
            for q in event.game_event:
                if q.id in player_check[p.id]["collisions"]:
                    player_check[p.id]["collisions"][q.id] += 1
                else:
                    player_check[p.id]["collisions"][q.id] = 1
    return player_check


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


def create_game_from_scheduler(league, game, flight=None):
    """
    This function creates a new game event for a given league using the information
    provided.

    Args:
        league (int): The `league` input parameter provides access to the league
            object which contains information such as clubs and their facilities.
        flight (int): The `flight` input parameter specifies the flight number of
            the game event.
        game (dict): The `game` input parameter is a dictionary containing information
            about the game to be created.

    """
    timeslot = league.get_timeslot_by_id(game["timeslot"])
    facility = league.club.get_facility_by_id(game["facility"])
    a_player = league.club.get_player_by_id(game["players"][0])
    if flight is None:
        flight = league.get_flight_for_player(a_player)
    if game["captain"] is not None:
        captain = league.club.get_player_by_id(game["captain"])
    else:
        captain = league.club.get_player_by_id(game["players"][0])
    players = []
    for p in game["players"]:
        players.append(league.club.get_player_by_id(p))
    league.create_game_event(players, facility, timeslot, flight, captain=captain)


def create_player_objects(flight, league, rules):
    """
    This function creates a list of `Player` objects from a flight's player
    associations and computes the mean availability score for the players based
    on league availability data.

    Args:
        flight (): The `flight` input parameter is a list of player associations
            from which the function creates players.
        league (dict): The `league` input parameter is used to retrieve player
            availability information for each player association.
        rules (dict): The `rules` input parameter defines the ruleset for player
            creation; it is used to initialise the player object's attributes like
            avg.

    Returns:
        list: The output returned by the `create_player_objects` function is a
        list of `Player` objects. Each `Player` object has an `id`, `rules`, and
        an `availability_score` attribute set based on the player's availability
        according to the `league` object's `get_player_availability_dict`. The
        `mean_availability_score` variable is computed as the average availability
        score of all players and each player's `availability_score` attribute is
        set relative to this mean.

    """
    players = []
    mean_availability_score = 0
    for a in flight.player_associations:
        avail = league.get_player_availability_dict(a.player)
        p = Player(a.player.id, rules, avail)
        mean_availability_score += p.availability_score
        players.append(p)
    mean_availability_score /= len(players)
    for p in players:
        p.set_availability_score_relation(mean_availability_score)
    return players


def create_gameslot_objects(league, rules):
    """
    This function creates a list of `GameSlot` objects based on the availability
    of facilities and timeslots for a given league.

    Args:
        league (): The `league` input parameter is a League object that provides
            information about the available timeslots and facility associations
            for scheduling games.
        rules (): The `rules` input parameter defines the game slot object's
            parameters and restrictions such as scoring format or duration constraints.

    Returns:
        list: The output returned by this function is a list of `GameSlot` objects.

    """
    gameslots = []
    for t in league.timeslots:
        for f in league.facility_associations:
            facility_is_available, _ = f.facility.is_available(t)
            if facility_is_available:
                gs = GameSlot(t.id, f.facility.id, t.since_y2k, rules)
                gameslots.append(gs)
    return gameslots
