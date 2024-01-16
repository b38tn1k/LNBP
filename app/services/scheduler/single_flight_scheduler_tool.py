from random import shuffle
from itertools import combinations
from .constants import *


def init_histories(players):
    """
    This function initializes the "other player history" attribute of each player
    with a zero value for all other players.

    Args:
        players (list): The `players` input parameter is a list of Player objects
            and it is used to loop over all the players In the game.

    """
    # print("Init Histories")
    for player in players:
        for p in players:
            player.other_player_history[p.id] = 0


def get_histories(potential_game):
    """
    This function calculates the sum of all history scores for each player against
    every other player's history scores.

    Args:
        potential_game (dict): The `potential_game` parameter is an iterable of
            players (e.g. a list of player objects) and represents the current
            state of the game being played.

    Returns:
        int: The output returned by this function is 0.

    """
    sum_history = 0
    for player in potential_game:
        for p in potential_game:
            sum_history += player.other_player_history[p.id]
    return sum_history


def check_potential_game_length(potential_game, rules):
    """
    This function checks if the potential game (i.e. the sequence of moves made
    so far) has reached the maximum allowed length according to the rules.

    Args:
        potential_game (str): The `potential_game` input parameter is passed to
            the `check_potential_game_length` function as a string representation
            of the potential game state.
        rules (int): The `rules` input parameter specifies the maximum length of
            the game.

    Returns:
        bool: The output returned by the function `check_potential_game_length`
        would be `True`.

    """
    return len(potential_game) != rules


def contains_players_already_scheduled(players_scheduled, potential_game):
    """
    This function checks if any of the players listed on `potential_game` are
    already scheduled to play a game by checking `players_scheduled`.

    Args:
        players_scheduled (): The `players_scheduled` input parameter is a list
            of players that have already been scheduled for games.
        potential_game (list): The `potential_game` input parameter is a list of
            players that might be added to the game.

    Returns:
        bool: The output returned by this function is `False`.

    """
    return any(player in players_scheduled for player in potential_game)


def player_fails_day_week_count(potential_game, day, week):
    """
    This function checks if a player has reached the maximum number of games allowed
    for a specific day and/or week within a potential game.

    Args:
        potential_game (list): The `potential_game` input parameter is an iterable
            of games that are being checked to see if the player has failed their
            daily or weekly quota.
        day (str): The `day` input parameter specifies which day of the week to
            check for game participation.
        week (int): The `week` input parameter is used to check if the number of
            games played by a player during that week reaches or exceeds their
            maximum allowed number of games for that week as defined by their rules.

    Returns:
        bool: The output returned by this function is `False`. The function loops
        through all players and checks if any player has reached the maximum number
        of games allowed for the current day or week. Since no player satisfies
        these conditions for both day and week specified as arguments (`day=3` and
        `week=12`), none of the players are disqualified and all return `False`.

    """
    for player in potential_game:
        day_count = player.days.count(day)
        week_count = player.weeks.count(week)
        if (
            day_count >= player.rules["max_games_day"]
            or week_count >= player.rules["max_games_week"]
        ):
            return True
    return False


def all_players_satisfied(potential_game):
    """
    This function checks whether all players have satisfied their minimum and
    maximum game requirements by checking the player's current game count against
    their rules and returns True if all satisfied or False if over-scheduled.

    Args:
        potential_game (list): The `potential_game` input parameter is a list of
            players and their rules for a proposed game schedule. It is used to
            check if the scheduled games for each player satisfy their rules (e.g.

    Returns:
        bool: The output returned by the `all_players_satisfied` function is `False`.

    """
    all_satisfied = True
    over_scheduled = False
    for player in potential_game:
        if player.game_count < player.rules["min_games_total"]:
            all_satisfied = False
        if player.game_count >= player.rules["max_games_total"]:
            over_scheduled = True
    return all_satisfied or over_scheduled


class SingleFlightScheduleTool:
    def __init__(self, flight_id, rules, players, gameslots):
        """
        This function initalizes an object of the class "Flight" by setting its
        instance variables "flight_id", "rules", "gameslots" and "players" with
        the provided parameters.

        Args:
            flight_id (int): The `flight_id` parameter is used to identify the
                specific flight for which the Tournament Director is being created.
            rules (dict): The `rules` input parameter is used to define the specific
                rules of the game that are relevant for the current flight.
            players (list): The `players` input parameter sorts the list of players
                based on their availability score (i.e., highest availability
                first) before initializing the game instance.
            gameslots (list): In this function `gameslots` is a list of `GamingSlot`
                objects that are shuffled before being stored into the instance
                variables `self.gameslots`.

        """
        self.flight_id = flight_id
        self.rules = rules

        shuffle(gameslots)
        self.gameslots = sorted(gameslots, key=lambda gs: gs.facility_id, reverse=True)
        self.gameslots = sorted(self.gameslots, key=lambda gs: gs.availability_score)
        print ([g.availability_score for g in self.gameslots])
        self.players = sorted(players, key=lambda player: player.availability_score)

    def generate_timeslot_player_pool(self):
        """
        This function generates a dictionary of time slot player pools for each
        available timeslot based on the availability of players and the rules configuration.

        Returns:
            dict: The output of the function is a dictionary of timeslot player
            pools and a set of all available timeslots.

        """
        ts = set([g.timeslot_id for g in self.gameslots])
        tpp = {}  # timeslot player pool
        for t in ts:
            tpp[t] = {}
            tpp[t]["all"] = [
                p for p in self.players if p.availability[t] != UNAVAILABLE
            ]
            tpp[t]["filtered"] = [
                p
                for p in tpp[t]["all"]
                if p.availability[t] == AVAILABLE
                or (p.availability[t] == UNK and self.rules["assumeBusy"] is False)
            ]
            tpp[t]["times"] = [g for g in self.gameslots if g.timeslot_id == t]
            tpp[t]["day"] = tpp[t]["times"][0].day_number
            tpp[t]["week"] = tpp[t]["times"][0].week_number
            tpp[t]["available_slots"] = min(
                len(tpp[t]["times"]), self.rules["max_concurrent_games"]
            )
            tpp[t]["sgames"] = []
            tpp[t]["pgames"] = []  # all potential games
            game_grabber = (
                tpp[t]["filtered"]
                if len(tpp[t]["filtered"]) > self.rules["players_per_match"]
                else tpp[t]["all"]
            )
            if len(game_grabber) >= self.rules["players_per_match"]:
                for g in combinations(tpp[t]["all"], self.rules["players_per_match"]):
                    tpp[t]["pgames"].append(g)
        return tpp, ts
    
    def initCA(self):
        """
        This function initializes the combat agent's player pool and histories
        using the `generate_timeslot_player_pool` and `init_histories` methods.
        It then shuffles the timeslot list to assign random positions to players.

        Returns:
            list: The function `initCA` returns two items:
            
            1/ A tuple of player objects `tpd` containing all the player objects.
            2/ A list `ts_list` of timeslot objects randomly shuffled.

        """
        init_histories(self.players)
        tpp, ts = self.generate_timeslot_player_pool()
        ts_list = list(ts)
        # shuffle(ts_list)
        return tpp, ts_list
    
    def schedule_games_for_timeslot(self, tpp, ts_list, all_scheduled_games):
        """
        This function schedules games for a given timeslot while ensuring that
        certain rules are satisfied. These rules include having available slots
        for the timeslot and not scheduling too many games for any one player or
        on any one day or week.

        Args:
            tpp (dict): The `tpp` input parameter is a dictionary that contains
                the current state of the timeslots for each player.
            ts_list (list): The `ts_list` input parameter is a list of tuples
                containing timeslot information (day and week) for which games are
                to be scheduled.
            all_scheduled_games (list): The `all_scheduled_games` input parameter
                is a list that accumulates all the scheduled games for each timeslot
                during the scheduling process. It is initially empty and is filled
                as the scheduling loop adds scheduled games to it at the end of
                each iteration.

        """
        while True:
            game_added = 0
            timeslot_count = 0
            already_added = False
            for t in ts_list:
                timeslot_count += 1
                # Track which players have already been scheduled
                players_scheduled = set([p for p in [g for g in tpp[t]["sgames"]]])
                # Game selection priority sorting
                sorted_games = sorted(tpp[t]["pgames"], key=lambda x: get_histories(x))
                already_added = False
                average_game_count = self.get_average_game_count()
                lower_than_average = []
                for g in sorted_games:
                    add_game = False
                    for p in g:
                        if p.game_count < average_game_count:
                            add_game = True
                    if add_game:
                        lower_than_average.append(g)
                if len(lower_than_average) != 0:
                    sorted_games = lower_than_average
                day, week = tpp[t]["day"], tpp[t]["week"]
                for potential_game in sorted_games:
                    # only consider 1 game per loop
                    if already_added:
                        break
                    # Apply Rule 1: Ensure we have available slots for this timeslot
                    if tpp[t]["available_slots"] == 0:
                        # failing_scenarios['available slots'] += 1
                        break

                    if check_potential_game_length(
                        potential_game, self.rules["players_per_match"]
                    ):
                        # failing_scenarios['game length'] += 1
                        continue

                    # Apply Rule 2: Check if any player in this game is already scheduled for this timeslot
                    if contains_players_already_scheduled(
                        players_scheduled, potential_game
                    ):
                        # failing_scenarios['players already scheduled'] += 1
                        continue

                    # Apply Rule 3: Count how many times the player has already played that day, week
                    if player_fails_day_week_count(potential_game, day, week):
                        # failing_scenarios['day or week failure'] += 1
                        continue

                    # Apply Rule 4: Don't schedule games where all players have a game_count > tempRules["min_games_total"]
                    # Apply Rule 5: Don't schedule games where any player has a game_count >= tempRules["max_games_total"]
                    if all_players_satisfied(potential_game):
                        # failing_scenarios['all players satisfied'] += 1
                        continue

                    # All constraints satisfied, so we schedule this game
                    tpp[t]["sgames"].append(potential_game)
                    tpp[t]["available_slots"] -= 1
                    game_added += 1
                    already_added = True

                    # Track all scheduled games also
                    all_scheduled_games.append(potential_game)

                    # Update tracking variables
                    for player in potential_game:
                        player.days.append(tpp[t]["day"])
                        player.weeks.append(tpp[t]["week"])
                        player.game_count += 1

                    for player in potential_game:
                        for p in potential_game:
                            if p is not player:
                                player.other_player_history[p.id] += 1
                    # At this point, tpp[t]['sgames'] contains some scheduled games for timeslot t
                    # only consider 1 game per loop
                    if already_added:
                        continue
            if game_added == 0:
                break

    def force_assign(self, tpp, ts_list):
        """
        This function takes a list of tuples `ts_list` and a dict of tournament
        pairs `ttpp`, and it forces player assignments to matches based on facility
        IDs.

        Args:
            tpp (dict): The `tpp` input parameter is a dictionary of tennis
                tournament schedules and it is used to store the tournament schedule
                data after sorting the times and forcing player-game matches.
            ts_list (dict): The `ts_list` input parameter is a list of dicts
                containing player data. Each dict represents a single player and
                contains the key "times" with a list of games played by that player.

        """
        for t in ts_list:
            tpp[t]["times"] = sorted(tpp[t]["times"], key=lambda x: x.facility_id)
            if len(tpp[t]["sgames"]) != 0:
                for i, sg in enumerate(tpp[t]["sgames"]):
                    gs = tpp[t]["times"][i]
                    for p in sg:
                        gs.force_player_to_match(p)

    def second_force_assign(self, third_iteration):
        for match in third_iteration:
            selected_gs = None
            for gs in match["overlap"]:
                if gs.full is False:
                    selected_gs = gs
            if selected_gs:
                for p in match["players"]:
                    selected_gs.force_player_to_match(p)
                    self.recalculate_players()

    def runCA(self):
        """
        This function is trying to resolve scheduling conflicts between players
        by matching them with games that are scheduled at the same time. It does
        this by iteratively grouping players into potential match groups based on
        the overlap of their preferences and existing game assignments.

        """
        print("Run CA")
        tpp, ts_list = self.initCA()
        all_scheduled_games = []
        print("schedule games")
        self.schedule_games_for_timeslot(tpp, ts_list, all_scheduled_games)
        self.recalculate_players()
        print("force assign")
        self.force_assign(tpp, ts_list)
        self.recalculate_players()

    def recalculate_players(self):
        """
        This function recalculates the game statistics and satisfaction of each
        player based on the current state of the gameslot and the player's history.

        """
        # print("Recalculate Players")
        satisfied = {}
        for p in self.players:
            satisfied[p.id] = 0
            p.days = []
            p.weeks = []
            p.game_count = 0
            for k in p.other_player_history:
                p.other_player_history[k] = 0
        for game in self.gameslots:
            if game.full:
                for p in game.game_event:
                    p.days.append(game.day_number)
                    p.weeks.append(game.week_number)
                    p.game_count += 1
                    satisfied[p.id] += 1
                    for q in game.game_event:
                        if p != q:
                            if q.id in p.other_player_history:
                                p.other_player_history[q.id] += 1
                            else:
                                p.other_player_history[q.id] = 1
        for p in self.players:
            p.satisfied = satisfied[p.id] >= p.rules["min_games_total"]

    def return_events(self):
        """
        This function returns a list of events for each gameslot that has a full
        roster of players.

        Returns:
            dict: The output returned by the `return_events` function is a list
            of dictionaries containing information about the game events that are
            happening at each time slot and facility.

        """
        events = []
        for gameslot in self.gameslots:
            if gameslot.full is True:
                captain = None
                if gameslot.captain is None:
                    captain = gameslot.game_event[0].id
                else:
                    captain = gameslot.captain.id
                events.append(
                    {
                        'timeslot': gameslot.timeslot_id,
                        'facility': gameslot.facility_id,
                        'captain': captain,
                        'players': [p.id for p in gameslot.game_event],
                    }
                )
        return events

    def all_players_satisfied(self):
        """
        This function checks whether all players (referenced by the 'players'
        attribute) have satisfied their condition (represented by the 'satisfied'
        attribute) and returns 'True' if all are satisfied or 'False' if at least
        one player is not satisfied.

        Returns:
            bool: The output returned by the function "all_players_satisfied" is
            "True".

        """
        for player in self.players:
            if player.satisfied == False:
                return False
        return True

    def get_average_game_count(self):
        """
        This function calculates the average game count of all players within the
        "self" context (presumably a collection or list of players).

        Returns:
            float: The output returned by this function would be a float value
            representing the average game count of all players belonging to the
            `self` object.

        """
        return sum([p.game_count for p in self.players]) / len(self.players)


    def assign_captains(self):
        """
        This function assigns a captain to each game slot that has a full team and
        doesn't already have a captain assigned.

        """
        assigned = set()
        self.recalculate_players()
        for p in self.players:
            p.captain_count = 0
        full_games_length = len([g for g in self.gameslots if g.full is True])
        shuffle(self.gameslots)
        for g in self.gameslots:
            if g.full is True:
                if g.captain is None:
                    for p in g.game_event:
                        if not p.id in assigned or len(assigned) == full_games_length:
                            g.captain = p
                            p.captain_count += 1
                            assigned.add(p.id)
                            self.recalculate_players()
                            break



