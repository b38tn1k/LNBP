from .single_flight_scheduler_tool import SingleFlightScheduleTool
from .constants import *
from .player import Player
from .gameslot import GameSlot


class Scheduler:
    SINGLE_FLIGHT = 0
    GENERATE_REPORT = 1

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

        if mode == self.GENERATE_REPORT:
            pass

        if mode == self.SINGLE_FLIGHT:
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
            flight = create_game_from_scheduler(self.league, e, flight=self.flight)
        return flight

    def evaluate(self, scheduler):
        """
        This function evaluates a given esports schedule and checks if each player
        violates any of the rules specified by the "tiers" dictionary. The rules
        are:
                - Minimum game count for each tier (e.g., at least 5 games for Tier 1)
                - Maximum game count for each tier (e.g., no more than 10 games for Tier
        2)
                - Captainhood requirements (at least 2 or at most 5 games as captain)
                - Preferred game scheduling (minimizing low-preference games)
                - Maximum number of games per week and day
                - Minimum gap between games (at least 1 day)
                - Limit on repeated competitions against other players (no more than 2
        games against the same player).
        If a player violates any of these rules at any tier level with which they
        are associated.

        Args:
            scheduler (dict): The `scheduler` input parameter is used to evaluate
                the player availability and scheduling constraints for each player.
                It provides the number of games each player can play during a given
                week and their preferred days to play those games.

        Returns:
            dict: The `evaluate` function returns a dictionary of broken rules
            counters and details for each player.

        """
        tiers = {}
        tiers["min_games_total"] = "tier1"
        tiers["max_games_total"] = "tier2"
        tiers["game_count"] = "tier1"

        tiers["min_captained"] = "tier2"
        tiers["max_captained"] = "tier2"
        tiers["captain_count"] = "tier2"

        tiers["overscheduled_lp"] = "tier2"

        tiers["max_week_gap"] = "tier2"
        tiers["max_games_week"] = "tier1"

        tiers["max_games_day"] = "tier1"

        tiers["max_repeat_compete"] = "tier2"
        max_repeat_compete = 0.5  # * game_count

        # tiers["players_per_match"] = "tier1"
        # tiers["minimum_subs_per_game"] = "tier1"

        player_check = summarize_schedule(scheduler)
        fails = {"tier1": 0, "tier2": 0, "details": []}  # rules broken counter

        for player in player_check:
            p = player_check[player]
            rules = p["rules"]
            # player satisfied
            if not p["satisfied"]:
                record_broken_rules(player, tiers, fails, "game_count")
            # player min game count
            if p["game_count"] < rules["min_games_total"]:
                record_broken_rules(player, tiers, fails, "min_games_total")
            # player max game count
            if p["game_count"] > rules["max_games_total"]:
                record_broken_rules(player, tiers, fails, "max_games_total")
            # captainhood
            captainhood_under = (
                p["captain_count"] < rules["min_captained"]
            )  # true is bad
            captainhood_over = p["captain_count"] >= rules["max_captained"]
            captainhood_ok = (not captainhood_under) and (
                not captainhood_over
            )  # false and false is good

            if not captainhood_ok:
                record_broken_rules(player, tiers, fails, "captain_count")

            if captainhood_under:
                record_broken_rules(player, tiers, fails, "min_captained")

            if captainhood_over:
                record_broken_rules(player, tiers, fails, "min_captained")

            # player mostly scheduled low preference
            over_scheduled_lp = (p[AVAILABLE_LP] * 2) > p["game_count"]
            if over_scheduled_lp:
                record_broken_rules(player, tiers, fails, "overscheduled_lp")

            # player week numbers
            last_week = None
            week_nums = p["week_numbers"]
            week_nums = {k: p["week_numbers"][k] for k in sorted(p["week_numbers"])}
            for n in week_nums:
                if week_nums[n] > rules["max_games_week"]:
                    record_broken_rules(player, tiers, fails, "max_games_week")
                if last_week is None:
                    last_week = n
                else:
                    gap = abs(n - last_week)
                    if gap > rules["max_week_gap"]:
                        record_broken_rules(player, tiers, fails, "max_week_gap")
                    last_week = n

            # player day numbers
            days = p["day_numbers"]
            for d in days:
                if days[d] > rules["max_games_day"]:
                    record_broken_rules(player, tiers, fails, "max_games_day")

            # player playing other player too many times
            collisions = p["collisions"]
            thresh = round(p["game_count"] * max_repeat_compete)
            for c in collisions:
                if collisions[c] > thresh and c != player:
                    record_broken_rules(
                        player, tiers, fails, "max_repeat_compete", notes=str(c)
                    )
        return fails

    def report(self):
        """
        This function generates a schedule for a fantasy league game week by
        resolving conflicts and finding the optimal games slots for each player
        based on their preferences and restrictions.

        """
        print("GENERATE REPORT")
        for flight in self.league.flights:
            # flight = self.league.get_flight_by_id(self.flight_id)
            gameslots = create_gameslot_objects(self.league, self.rules, check=False)
            players = create_player_objects(flight, self.league, self.rules)
            generateGameSlotAvailabilityScores(gameslots, players)
            player_dict = {}
            for p in players:
                player_dict[p.id] = p
            gameslots_dict = {}
            for gs in gameslots:
                if gs.facility_id in gameslots_dict:
                    gameslots_dict[gs.facility_id][gs.timeslot_id] = gs
                else:
                    gameslots_dict[gs.facility_id] = {}
                    gameslots_dict[gs.facility_id][gs.timeslot_id] = gs

            for event in flight.game_events:
                fid = event.facility_id
                tid = event.timeslot_id
                if fid in gameslots_dict:
                    if tid in gameslots_dict[fid]:
                        gs = gameslots_dict[fid][tid]
                        for p in event.players:
                            gs.force_player_to_match(player_dict[p.id])
                        gs.captain = player_dict[event.captain.id]
                        gs.captain.captain_count += 1
            scheduler = SingleFlightScheduleTool(flight.id, self.rules, players, gameslots, 0)
            scheduler.finalize()
            # print('new')
            res = self.evaluate(scheduler)
            report = []
            for d in sorted(res["details"], key=lambda x: x["tier"]):
                r = parse_violation_human_readable(self.league, d)
                print(r)
                if r is not None:
                    report.append(r)
            flight.report = report
            print("DONE")

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
                scheduler.optimise()
                scheduler.assign_captains()
                scheduler.finalize()
                res = self.evaluate(scheduler)
                # print(res)
                # print()
                candidates.append({"scheduler": scheduler, "res": res})
        best_candidate = min(
            candidates, key=lambda x: (x["res"]["tier1"], x["res"]["tier2"])
        )
        # print()
        # print(best_candidate)
        report = []
        for d in sorted(best_candidate["res"]["details"], key=lambda x: x["tier"]):
            r = parse_violation_human_readable(self.league, d)
            if r is not None:
                report.append(r)
        flight = self.build(best_candidate["scheduler"])
        flight.report = report


def parse_violation_human_readable(league, violation):
    """
    This function takes a league object and a violation object as inputs and returns
    a human-readable string indicating the nature of the violation.

    Args:
        league (): The `league` input parameter passes a reference to the Fantasy
            Premier League object that contains all the teams and players' data
            for the given league.
        violation (dict): The `violation` input parameter represents a dict
            containing various key-value pairs representing different league
            violations found during the scheduling process.

    Returns:
        str: The output returned by this function is a human-readable string
        indicating the violation of a league's rules.

    """
    messages = {}
    messages["min_games_total"] = "does not have enough games."
    messages["max_games_total"] = "is playing more games than required."
    # messages["game_count"] = "tier1"
    messages["min_captained"] = "does not captain enough games."
    messages["max_captained"] = "captains more games than required"
    # messages["captain_count"] = "tier2"
    messages[
        "overscheduled_lp"
    ] = "has more than half their schedule in low preference timeslots"
    messages["max_week_gap"] = "has a large gap in weeks played."
    messages["max_games_week"] = "plays too many times in a week."
    messages["max_games_day"] = "plays too many times in a day."

    player = league.club.get_player_by_id(violation["player"])
    my_string = None
    if violation["broken_rule"] in messages:
        my_string = player.full_name + " " + messages[violation["broken_rule"]]
    if "max_repeat_compete" in violation["broken_rule"]:
        other_player_id = int(violation["broken_rule"].split(":")[-1])
        other_player = league.club.get_player_by_id(other_player_id)
        my_string = (
            player.full_name
            + " is matched with "
            + other_player.full_name
            + " for more than half their games."
        )

    return my_string


def record_broken_rules(player, tiers, record, rule, notes=None):
    """
    This function records instances of a player breaking specific rules
    (represented by a string `rule`) within designated tiers (`tiers`), and
    keeps track of the number of times each rule is broken at each tier.

    Args:
        player (str): The `player` input parameter passes on the player object
            related to a multiplayer game as an identifier that distinguishes
            different players' actions or behaviors.
        tiers (dict): The `tiers` input parameter is a dictionary that maps
            each rule to its corresponding tier (a value between 1 and 5).
        record (dict): The `record` input parameter is a dictionary that is
            updated with the current values of broken rules and their tiers.
        rule (str): The `rule` parameter specifies the specific broken rule
            being recorded.
        notes (str): The `notes` input parameter appends a colon and the given
            string to the end of the `rule` string when it is not None.

    """
    t = tiers[rule]
    record[t] += 1
    if notes is not None:
        rule += ":" + notes
    record["details"].append({"player": player, "broken_rule": rule, "tier": t})


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
            "game_count": player.game_count,
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
    return flight


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


def create_gameslot_objects(league, rules, check=True):
    """
    This function creates a list of GameSlot objects for all possible combinations
    of time slots and facilities available for the given league.

    Args:
        league (): The `league` input parameter is passed a `League` object
            containing information about the league such as its name and time slots
            available.
        rules (dict): The `rules` input parameter specifies the game rules to be
            used when creating game slots.
        check (bool): The `check` input parameter allows the creation of GameSlots
            only if a facility is available. If `check=True`, the function checks
            for facility availability before creating a GameSlot.

    Returns:
        list: The output of this function is a list of GameSlot objects.

    """
    gameslots = []
    for t in league.timeslots:
        for f in league.facility_associations:
            # Check facility availability only if 'check' is True, otherwise assume availability
            if not check or f.facility.is_available(t)[0]:
                gs = GameSlot(t.id, f.facility.id, t.since_y2k, rules)
                gameslots.append(gs)
    return gameslots
