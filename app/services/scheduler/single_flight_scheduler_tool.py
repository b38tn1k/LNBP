from random import shuffle
from itertools import combinations
from .constants import *
import math


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


def all_players_above_average(potential_game, games, players):
    """
    The function `all_players_above_average` checks if all players In the
    'potential_game' list have more games than the average number of games played
    by all players In the 'games' list.

    Args:
        potential_game (dict): The `potential_game` input parameter is not used
            at all by the function `all_players_above_average`. It is passed as
            an argument to the function but never references or acted upon inside
            the function's body.
        games (list): The `games` input parameter is the list of games that are
            being analyzed for the above-average players.
        players (list): The `players` input parameter is a list of players and its
            purpose is to pass it as an argument to the `for player` loop inside
            the function.

    Returns:
        bool: Based on the given function code and input data (i.e., `potential_game`
        and `players`), the output returned by the function is `True`.

    """
    avg_games = len(games) / len(players) + 0.5
    for player in potential_game:
        if player.game_count < avg_games:
            return False
    return True


def shift_blocks(arr, mutate):
    """
    This function shifts the items of an array by a specified number of groups
    based on their availability score.

    Args:
        arr (list): The `arr` input parameter is the original array that needs to
            be reordered based on the availability scores.
        mutate (int): The `mutate` input parameter specifies the number of groups
            to reverse at the end of the function.

    Returns:
        list: The output returned by this function is a new array that is created
        by reverseing the order of the first 'mutate' groups based on the availability
        score and extending it with the rest of the items.

    """
    if not arr or mutate <= 0:
        return arr
    mutate += 1

    # Grouping items by availability_score
    score_groups = {}
    for item in arr:
        score = item.availability_score
        score_groups.setdefault(score, []).append(item)

    # Sorting the dictionary keys (availability scores)
    sorted_scores = sorted(score_groups.keys())

    # Determine the number of groups to reverse
    num_groups = len(sorted_scores)
    mutate %= num_groups
    if mutate == 0:
        return arr

    # Reversing the order of the first 'mutate' groups
    reversed_scores = list(reversed(sorted_scores[:mutate])) + sorted_scores[mutate:]

    # Building the new array
    new_arr = []
    for score in reversed_scores:
        new_arr.extend(score_groups[score])

    return new_arr


def interlace_and_rotate(arr, mutate):
    """
    This function takes an input array and a mutation number (%), and returns a
    new rotated version of the array by:
    1/ Splitting the input array into two halves.
    2/ Interleaving elements from the second half into the first half.
    3/ Rotating the rearranged array by the mutation number (%).

    Args:
        arr (list): The `arr` input parameter is the main input array that is to
            be interlaced and rotated.
        mutate (int): The `mutate` parameter modifies the final result of the
            function by rotating the interleaved array by a certain number of
            elements (limited by the length of the array).

    Returns:
        list: The output returned by this function is a rotation and interleaving
        of the input array `arr`, where the length of the rotation is specified
        by the parameter `mutate`.

    """
    if not arr:
        return arr

    length = len(arr)
    # Step 1: Rearranging the array
    # Split the array into two halves
    first_half = arr[: length // 2]
    second_half = arr[length // 2 :]
    if length % 2:
        second_half.append(None)  # Append None if the array has odd length

    # Interleave elements from the second half into the first half
    rearranged = [
        val
        for pair in zip(first_half, reversed(second_half))
        for val in pair
        if val is not None
    ]

    # Step 2: Rotating the array
    mutate %= length  # Handle cases where mutate is larger than the array length
    rotated = rearranged[-mutate:] + rearranged[:-mutate]

    return rotated


class SingleFlightScheduleTool:
    def __init__(self, flight_id, rules, players, gameslots, mutate):
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
        self.gameslots = gameslots
        self.mutate = mutate
        self.mutate_mode = ""

        # shuffle(gameslots)
        # self.gameslots = sorted(gameslots, key=lambda gs: gs.facility_id, reverse=True)
        # self.gameslots = sorted(self.gameslots, key=lambda gs: gs.availability_score)
        # self.gameslots = shift_blocks(self.gameslots, mutate)

        # print([g.availability_score for g in self.gameslots])
        # print()
        # print([g.timeslot_id for g in self.gameslots])
        # print()
        self.players = sorted(players, key=lambda player: player.availability_score)
        self.players = shift_blocks(self.players, mutate)

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
        This function initializes the player pool and histories
        using the `generate_timeslot_player_pool` and `init_histories` methods.
        It then shuffles the timeslot list to assign random positions to players.

        Returns:
            list: The function `initCA` returns two items:

            1/ A tuple of player objects `tpd` containing all the player objects.
            2/ A list `ts_list` of timeslot objects randomly shuffled.

        """
        init_histories(self.players)
        tpp, ts = self.generate_timeslot_player_pool()
        self.gameslots = sorted(self.gameslots, key=lambda gs: gs.availability_score)
        if self.mutate < len(ts):
            self.gameslots = shift_blocks(self.gameslots, self.mutate)
            self.mutate_mode = "Availability score ordered shift"
            # print("SHIFTER")
        elif self.mutate > 2 * len(ts):
            shuffle(self.gameslots)
            self.mutate_mode = "Random shuffle"
            # print("SHUFFLER")
        else:
            self.mutate_mode = "Interlace and rotate"
            self.gameslots = interlace_and_rotate(self.gameslots, self.mutate - len(ts))
        ts_list = []
        seen = set()
        for item in self.gameslots:
            if item.timeslot_id not in seen:
                seen.add(item.timeslot_id)
                ts_list.append(item.timeslot_id)
        return tpp, ts_list

    def finalize(self):
        """
        The `finalize()` function recalculates the players' values.

        """
        self.recalculate_players()

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
        allowable_skips = 10
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
                allowable_skips -= 1
            if allowable_skips == 0:
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

    def run(self):
        """
        This function is trying to resolve scheduling conflicts between players
        by matching them with games that are scheduled at the same time. It does
        this by iteratively grouping players into potential match groups based on
        the overlap of their preferences and existing game assignments.

        """
        # print("Run CA")
        tpp, ts_list = self.initCA()
        all_scheduled_games = []
        # print("schedule games")
        self.schedule_games_for_timeslot(tpp, ts_list, all_scheduled_games)
        self.recalculate_players()
        # print("force assign")
        self.force_assign(tpp, ts_list)

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
        i = 0
        for game in self.gameslots:
            if game.full:
                i += 1
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
        self.recalculate_players()
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
                        "timeslot": gameslot.timeslot_id,
                        "facility": gameslot.facility_id,
                        "captain": captain,
                        "players": [p.id for p in gameslot.game_event],
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
        counter = 0
        while counter < 50:
            good = True
            assigned = set()
            self.recalculate_players()
            for p in self.players:
                p.captain_count = 0
            for g in self.gameslots:
                if g.full is True:
                    g.captain = None
            shuffle(self.gameslots)
            for g in self.gameslots:
                if g.full is True:
                    if g.captain is None:
                        for p in g.game_event:
                            if not p.id in assigned:
                                g.captain = p
                                p.captain_count += 1
                                assigned.add(p.id)
                                break
                        if g.captain is None:
                            good = False
                            counter += 1
            if good is True:
                break

    def get_underover_scheduled_players(self):
        """
        This function returns two lists of players: "underscheduled" and "overscheduled".

        Returns:
            list: The output returned by this function is a tuple containing two
            lists:

                - `underscheduled`: a list of players who have played less than their
            minimum number of games specified by their rules.
                - `overscheduled`: a list of players who have played more than their
            maximum number of games specified by their rules.

        """
        underscheduled = []
        overscheduled = []
        for p in self.players:
            if p.game_count < p.rules["min_games_total"]:
                underscheduled.append(p)
            if p.game_count > p.rules["max_games_total"]:
                overscheduled.append(p)
        return underscheduled, overscheduled

    def fix_unscheduled_players(self):
        # find unsatisfied players
        """
        This function "fix_unscheduled_players" takes a list of players and resolves
        the unsatisfied player problem by grouping under- or over-scheduled players
        together and matching them with other available players based on common timeslots.

        """
        self.recalculate_players()
        underscheduled, overscheduled = self.get_underover_scheduled_players()
        if len(underscheduled) == 0:
            return True
        common_timeslots = {}
        for p in underscheduled:
            for timeslot_id, availability in p.availability.items():
                if availability in [AVAILABLE, AVAILABLE_LP]:
                    if timeslot_id in common_timeslots:
                        common_timeslots[timeslot_id].append(p)
                    else:
                        common_timeslots[timeslot_id] = [p]
        for id in common_timeslots:
            if len(common_timeslots[id]) >= self.rules["players_per_match"]:
                gs = [
                    g for g in self.gameslots if g.timeslot_id == id and g.full == False
                ]
                if gs:
                    new_game = gs[0]
                    best_game = []
                    for g in gs:
                        bad_score = 0
                        candidates = []
                        for p in common_timeslots[id]:
                            if not g.day_number in p.days and not g.week_number in p.weeks:
                                if p.availability[g.timeslot_id] == AVAILABLE:
                                    candidates.append(p)
                            if g.day_number in p.days:
                                bad_score += 1
                            if g.week_number in p.weeks:
                                bad_score += 1
                        best_game.append({'score': bad_score, 'game': g, 'candidates' : candidates})
                    lowest_score_game = min(best_game, key=lambda x: x['score'])
                    added = False
                    for s in best_game:
                        if len(s['candidates']) >= self.rules['players_per_match']:
                            added = True
                            for p in s['candidates']:
                                s['game'].force_player_to_match(p)
                            break
                    if added is False and lowest_score_game['game']:
                        for p in common_timeslots[id]:
                            lowest_score_game['game'].force_player_to_match(p)
        self.recalculate_players()
        underscheduled, _ = self.get_underover_scheduled_players()
        return len(underscheduled) == 0

    def fix_double_players(self):
        # find double day players
        """
        This function attempts to resolve double header conflicts for a list of
        players by finding potential games for each conflicted player to swap with
        and then swapping the games if possible.

        Returns:
            None: The output of this function is `True` if it successfully swapped
            games for any double-headed players and `False` otherwise.

        """
        self.recalculate_players()
        double_headed_players = []

        # collect trouble makers
        for p in self.players:
            if len(p.days) != len(set(p.days)):
                double_headed_players.append(p)
        if len(double_headed_players) == 0:
            return

        # if (
        #     len(double_headed_players) > len(self.players) / 2
        # ):  # if it is going to be too much work, just give up
        #     return False

        c = {}  # candidate ts and data collector, days first cause it might fix weeks

        for p in double_headed_players:
            c[p.id] = {
                "candidates": [],
                "already_scheduled": set(),
                "duplicates": [],
                "player": p,
            }
            counter = {}
            for day in p.days:
                c[p.id]["already_scheduled"].add(day)
                if day in counter:
                    counter[day] += 1
                else:
                    counter[day] = 1
            for week in p.weeks:
                c[p.id]["already_scheduled"].add(week)

            c[p.id]["duplicates"] = [
                item for item in counter if counter[item] > p.rules["max_games_day"]
            ]  # finding the day we need to reduce games in

        day_number_lookup = {}
        for g in self.gameslots:
            if g.full is True:
                # organise games by day and week number
                if g.day_number in day_number_lookup:
                    day_number_lookup[g.day_number].append(g)
                else:
                    day_number_lookup[g.day_number] = [g]
                # is it a candidate for swapping?
                for p in double_headed_players:
                    pa = p.availability[g.timeslot_id]
                    pas = g.day_number in c[p.id]["already_scheduled"]
                    pasw = g.week_number in c[p.id]["already_scheduled"]
                    pig = p in g.game_event
                    if pa != UNAVAILABLE and not pas and not pasw and not pig:
                        c[p.id]["candidates"].append(g)

        # at this point, I have a dictionary c which includes
        #   - all players with double header days,
        #   - all other created games they could be in
        #   - the game slot day number for which they have a duplicate
        for p in double_headed_players:
            # 1. find a game slot in the duplicate
            for dp in c[p.id]["duplicates"]:
                source = None
                for g in day_number_lookup[dp]:
                    if g.player_in_game(p):
                        source = g
                        break
                if source:  # 2. find other players that could make a game swap
                    swap_candidates = []
                    for gc in c[p.id]["candidates"]:  # game candidates
                        for op in gc.game_event:  # other players
                            if (
                                op.availability[source.timeslot_id] != UNAVAILABLE
                                and op not in double_headed_players
                                and source.week_number not in op.weeks
                            ):
                                swap_candidates.append(
                                    {"p": op, "g": gc}
                                )  # other players and the candidate game they woudl swap from
                    source.swap_with_best_candidate(p, swap_candidates)
                    self.recalculate_players()

    def get_available_games_for_player(self, player):
        """
        This function retrieves a list of available games for a given player by
        filtering the game slots that satisfy the following conditions:
        1/ The player has availability for the game slot.
        2/ The game slot is not already full.
        3/ The game slot does not have any other players playing on it.

        Args:
            player (): The `player` input parameter passes a GamePlayer object to
                the get_available_games_for_player() function and supplies details
                about availability and participation of a specific player.

        Returns:
            list: The function returns a list of available games for the given player.

        """
        games = []
        for g in self.gameslots:
            pa = player.availability[g.timeslot_id] == AVAILABLE
            pin = g.player_in_game(player)
            if pa and g.full and not pin:
                games.append(g)
        return games
    
    def get_possible_games_for_player(self, player):
        """
        This function get_possible_games_for_player() takes a player object as
        input and returns a list of games that the player can play.

        Args:
            player (): The `player` input parameter passed to the function
                `get_possible_games_for_player` is used to filter which games are
                possible for that specific player.

        Returns:
            list: The output of this function is a list of `Game` objects for which
            the given `player` has availability and the game is not full.

        """
        games = []
        for g in self.gameslots:
            pa = player.availability[g.timeslot_id] != UNAVAILABLE
            pin = g.player_in_game(player)
            if pa and g.full and not pin:
                games.append(g)
        return games
    
    

    def get_available_players_for_game(self, game):
        """
        This function retrieves a list of available players for a given game by
        iterating through the list of all players and checking if they are available
        during the specific time slot and not already playing the game.

        Args:
            game (): The `game` input parameter is used to specify the game for
                which the available players are being requested.

        Returns:
            list: The output returned by the `get_available_players_for_game()`
            function is a list of available players for a given game.

        """
        players = []
        for p in self.players:
            pa = p.availability[game.timeslot_id] == AVAILABLE
            pin = game.player_in_game(p)
            if pa and not pin:
                players.append(p)
        return players

    def fix_lp_schedules(self):
        """
        This function `fix_lp_schedules` is trying to resolve minor conflicts
        between player-game assignments by swapping players and games that have
        minimal conflicts. It iterates over the available games for a given player
        and checks if there are any conflicting games (i.e., same day or week) and
        then checks if there are any conflicting players (i.e., same day or week).
        If there are no conflicts found for both players and games and the two
        entities can be matched successfully.

        """
        self.recalculate_players()
        minor_conflicts = []
        for g in self.gameslots:
            if g.full is True:
                for p in g.game_event:
                    if p.availability[g.timeslot_id] == AVAILABLE_LP:
                        minor_conflicts.append({"player": p, "game": g})
        mcfilter = {}
        for mc in minor_conflicts:
            if mc['player'].id in mcfilter:
                mcfilter[mc['player'].id] += 1
            else:
                mcfilter[mc['player'].id] = 1

        for mc in minor_conflicts:
            player = mc["player"]
            if mcfilter[player.id] < (player.game_count)/2:
                continue
            game = mc["game"]
            uf_games_for_player = self.get_available_games_for_player(player)
            filtered_gfp = []
            for g in uf_games_for_player:
                day_collision = (
                    g.day_number in player.days and g.day_number != game.day_number
                )
                week_collision = (
                    g.week_number in player.weeks and g.week_number != game.week_number
                )
                if not day_collision and not week_collision:
                    filtered_gfp.append(g)

            filtered_pfg = []
            if len(filtered_gfp) != 0:
                uf_player_for_games = self.get_available_players_for_game(game)
                for p in uf_player_for_games:
                    day_collision = game.day_number in p.days
                    week_collision = game.week_number in p.weeks
                    if not day_collision and not week_collision:
                        filtered_pfg.append(p)
            candidates = []
            if len(filtered_pfg) != 0:
                # print(len(filtered_gfp), len(filtered_pfg))
                for g in filtered_gfp:
                    for p in filtered_pfg:
                        if g.player_in_game(p):
                            candidates.append({"p": p, "g": g})
            if len(candidates) != 0:
                game.swap_with_best_candidate(p, candidates)
                self.recalculate_players()

    def balance_unscheduled_players(self):
        """
        This function balance_unscheduled_players() aims to distribute unscheduled
        players evenly among the games. It first calculates the average number of
        games played by each player and then identifies the under-scheduled players
        who have fewer games than the average. It then finds potential swappers
        (i.e., over-scheduled players) who can be matched with these under-scheduled
        players to balance out their game count.

        """
        self.recalculate_players()
        underscheduled, overscheduled = self.get_underover_scheduled_players()
        gc = [p.game_count for p in underscheduled]
        if len(gc) == 0:
            return
        average = math.ceil(sum(gc)/len(gc))
        freebies = [p for p in underscheduled if p.game_count < average] #players who get a game at the expense of other scheduled players
        for p in freebies:
            games = self.get_possible_games_for_player(p)
            ideas = []
            for g in games:
                added = False
                if g.day_number not in p.days and g.week_number not in p.weeks:
                    swapper = None
                    cands = [p for p in g.game_event if p.game_count >= p.rules['max_games_total']]
                    iovs = False
                    for innocent in cands:
                        if innocent.game_count > innocent.rules['max_games_total']:
                            swapper = innocent
                            iovs = True
                    if swapper is None and cands:
                        swapper = max(cands, key=lambda x: x.availability_score)
                    if swapper:
                        ideas.append({'player': swapper, 'overscheduled': iovs, 'target_game': g, 'availability_score': swapper.availability_score})
                
            if ideas:
                target = ideas[0]
                for i in ideas:
                    # print("swap", p.id, 'game count',p.game_count, "to", i['target_game'].timeslot_id, "replacing", i['player'].id, 'who has ascore', i['player'].availability_score, 'game count', i['player'].game_count)
                    if i['overscheduled'] is True:
                        target = i
                        break
                    if i['player'].availability_score > target['player'].availability_score:
                        target = i
                target['target_game'].remove_player_from_match(ideas[0]['player'])
                target['target_game'].force_player_to_match(p)

    def optimise(self):
        """
        This function optimises the game schedule by recalculating players and
        fixing unscheduled players.

        """
        self.recalculate_players()
        self.balance_unscheduled_players()
        keep_trying = self.fix_unscheduled_players()
        self.fix_double_players()
        # if keep_trying:
        #     self.fix_double_players()
        #     # self.fix_lp_schedules()
            
