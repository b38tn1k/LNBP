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


def contains_high_game_count_player(potential_game, average_game_count):
    """
    This function takes two arguments: `potential_game` and `average_game_count`,
    and returns a boolean value indicating if any player within the `potential_game`
    has a game count higher than the `average_game_count`.

    Args:
        potential_game (list): The `potential_game` parameter is a game that may
            contain one or more players to check if any of them have a high game
            count compared to the `average_game_count`.
        average_game_count (int): The `average_game_count` parameter is a threshold
            used to determine whether a player has a high game count or not.

    Returns:
        bool: The output returned by this function is `True` if there exists a
        player with more than `average_game_count` games among the players of the
        given `potential_game`.

    """
    return any(player.game_count > average_game_count for player in potential_game)


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


def get_play_count(potential_game):
    """
    This function takes a list of players and calculates the total number of games
    played by each player across all games involving those players. It does this
    by iterating over the players and summing their individual game counts. The
    final return value is the sum of these sums.

    Args:
        potential_game (list): The `potential_game` input parameter is a list of
            players and represents the possible game or set of games for which the
            function needs to calculate the play count.

    Returns:
        int: The output returned by the function `get_play_count` is `sum_history`,
        which is equal to the sum of the game counts of all players In the list `potential_game`.

    """
    sum_history = 0
    for player in potential_game:
        for p in potential_game:
            sum_history += player.game_count
    return sum_history


def create_failure_scenarios():
    """
    This function creates a dictionary of failure scenarios for a scheduling system.

    Returns:
        dict: The output returned by this function is an empty dictionary {}.

    """
    failing_scenarios = {}
    failing_scenarios["available slots"] = 0
    failing_scenarios["game length"] = 0
    failing_scenarios["players already scheduled"] = 0
    failing_scenarios["day or week failure"] = 0
    failing_scenarios["all players satisfied"] = 0
    return failing_scenarios


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
        self.players = sorted(players, key=lambda player: player.availability_score)

    def check_escape_conditions(self, log=False):
        """
        This function checks if a player satisfies the escape conditions of their
        schedule by checking for too many games played overall and per day and per
        week.

        Args:
            log (bool): The `log` input parameter is a Boolean that controls whether
                the function prints out messages to the console indicating which
                conditions are not met.

        Returns:
            bool: Based on the code provided and assuming that all player objects
            have their properties defined and satisfy the conditions checked by
            the function (i.e., no players have satisfied = True or game_count >
            rules["max_games_total"]), the output returned by this function would
            be:
            
            True

        """
        for player in self.players:
            # players have min games
            if player.satisfied == False:
                if log:
                    print("player satisfied")
                return False
            # players aren't over scheduled
            if player.game_count > player.rules["max_games_total"]:
                if log:
                    print("max games")
                return False
            for k in player.other_player_history:
                if player.other_player_history[k] >= 3:
                    if log:
                        print("bad history")
                    return False
            # players have days
            days = {}
            for day in player.days:
                if day in days:
                    days[day] += 1
                else:
                    days[day] = 1
            for key in days:
                if days[key] > player.rules["max_games_day"]:
                    if log:
                        print("max games")
                    return False
            # players have weeks
            weeks = {}
            for w in player.weeks:
                if w in weeks:
                    weeks[w] += 1
                else:
                    weeks[w] = 1
            for key in weeks:
                if weeks[key] > player.rules["max_games_week"]:
                    if log:
                        print("max weeks")
                    return False
        return True

    def check_all_conditions(self):
        """
        This function checks if a player has satisfied all the conditions specified
        by their rules object. It does this by looping through each day and week
        of the player's history and checking that no single day or week contains
        too many games according to the player's maximum game limits for those
        periods. If any of these conditions are not met (i.e., a player has satisfied
        all their conditions), the function returns True.

        Returns:
            bool: The output returned by this function is "True" if all conditions
            are met and "False" otherwise.

        """
        for player in self.players:
            if player.satisfied == False:
                return False
            if player.game_count > player.rules["max_games_total"]:
                return False
            for k in player.other_player_history:
                if player.other_player_history[k] >= 3:
                    return False
            days = {}
            for day in player.days:
                if day in days:
                    days[day] += 1
                else:
                    days[day] = 1
            for key in days:
                if days[key] > player.rules["max_games_day"]:
                    return False

            weeks = {}
            for w in player.weeks:
                if w in weeks:
                    weeks[w] += 1
                else:
                    weeks[w] = 1
            for key in weeks:
                if weeks[key] > player.rules["max_games_week"]:
                    return False
        return True

    def generate_timeslot_player_pool(self):
        """
        This function generates a dictionary of time slot player pools for each
        available timeslot based on the availability of players and the rules configuration.

        Returns:
            dict: The output of the function is a dictionary of timeslot player
            pools and a set of all available timeslots.

        """
        # print("Generate Time Slot Player Pool")
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

    def runCA(self):
        """
        This function is trying to resolve scheduling conflicts between players
        by matching them with games that are scheduled at the same time. It does
        this by iteratively grouping players into potential match groups based on
        the overlap of their preferences and existing game assignments.

        """
        # print("Run CA")
        tpp, ts = self.generate_timeslot_player_pool()
        ts_list = list(ts)
        shuffle(ts_list)
        all_scheduled_games = []
        init_histories(self.players)
        total_games_added = 0
        loop_count = 0
        games_considered = 0
        # print("Start Loop")
        while True:
            game_added = 0
            timeslot_count = 0
            loop_count += 1
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
                    games_considered += 1
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
                    total_games_added += 1
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
        self.recalculate_players()

        counter = 0
        for t in ts_list:
            tpp[t]["times"] = sorted(tpp[t]["times"], key=lambda x: x.facility_id)
            if len(tpp[t]["sgames"]) != 0:
                for i, sg in enumerate(tpp[t]["sgames"]):
                    gs = tpp[t]["times"][i]
                    counter += 1
                    for p in sg:
                        gs.force_player_to_match(p)

        self.recalculate_players()
        for p in self.players:
            _ = p.find_potential_slots_in_current_layout(self.gameslots)

        unsatisfied = [p for p in self.players if p.satisfied is False]
        counter = 0
        unsatisfied_friends = []
        second_iteration = []
        third_iteration = []
        while counter < len(unsatisfied) - 2:
            common_elments = set(unsatisfied[counter].potentials)
            common_elments.intersection_update(unsatisfied[counter + 1].potentials)
            if len(common_elments) != 0:
                unsatisfied_friends.append(
                    {
                        "players": [unsatisfied[counter], unsatisfied[counter + 1]],
                        "overlap": common_elments,
                    }
                )
            counter += 1
        if len(unsatisfied_friends) != 0:
            f2_old = unsatisfied_friends[0]["players"][1]
            f_old = unsatisfied_friends[0]
            for f in unsatisfied_friends:
                if f2_old == f["players"][0]:
                    common_elments = set(f["overlap"])
                    common_elments.intersection_update(f_old["overlap"])
                    if len(common_elments) != 0:
                        new_group = {
                            "players": [
                                f_old["players"][0],
                                f_old["players"][1],
                                f["players"][1],
                            ],
                            "overlap": common_elments,
                        }
                        second_iteration.append(new_group)
                f2_old = f["players"][1]
                f_old = f
        if len(second_iteration) != 0:
            f3_old = second_iteration[0]["players"][1]
            f_old = second_iteration[0]
            to_remove = []
            for gr in second_iteration:
                if f3_old == gr["players"][0]:
                    common_elments = set(f["overlap"])
                    common_elments.intersection_update(f_old["overlap"])
                    if len(common_elments) != 0:
                        p1 = [p for p in f_old["players"]]
                        p2 = [p for p in gr["players"]]
                        for np in p2:
                            if not np in p1:
                                p1.append(np)
                        new_group = {"players": p1, "overlap": common_elments}
                        third_iteration.append(new_group)
                        to_remove.append(f_old)
                        to_remove.append(gr)
                f3_old = gr["players"][1]
                f_old = gr
                for d in to_remove:
                    if d in second_iteration:
                        second_iteration.remove(d)

        for match in third_iteration:
            selected_gs = None
            for gs in match["overlap"]:
                if gs.full is False:
                    selected_gs = gs
            if selected_gs:
                for p in match["players"]:
                    selected_gs.force_player_to_match(p)
                    self.recalculate_players()

    def summarise_tests(self):
        """
        This function collects information about various satisfaction metrics for
        all players and returns a dictionary containing the results.

        Returns:
            dict: The function `summarise_tests` returns a dictionary containing
            four keys:
            
            	- `all_players_satisfied`: the value of the method `self.all_players_satisfied()`
            	- `player_days_satisfied`: the value of the method `self.player_days_satisfied()`
            	- `player_weeks_satisfied`: the value of the method `self.player_weeks_satisfied()`
            	- `no_players_overscheduled`: the value of the method `self.no_players_overscheduled()`
            
            So the output returned by this function is a dictionary with four values.

        """
        result = {}
        result["all_players_satisfied"] = self.all_players_satisfied()
        result["player_days_satisfied"] = self.player_days_satisfied()
        result["player_weeks_satisfied"] = self.player_weeks_satisfied()
        result["no_players_overscheduled"] = self.no_players_overscheduled()
        return result

    def backup_gameslots(self):
        """
        The `backup_gameslots()` function creates a list of copies of all the
        gameslots (represented by the variable `g` inside the function) and returns
        the list.

        Returns:
            list: The function `backup_gameslots` returns a list of copies of all
            the gameslots within the object `self`, each copied with its associated
            events.

        """
        b = []
        for g in self.gameslots:
            b.append(g.copy_with_events())
        return b

    def quick_log_game_count(self):
        """
        This function returns a string representing the number of games played by
        each player separated by spaces.

        Returns:
            str: The output returned by this function is "1 2 3".

        """
        myString = ""
        for p in self.players:
            myString += str(p.game_count) + " "
        return myString.strip()

    def clear_everything(self):
        """
        This function clears all game slots and recalculates the players.

        """
        for g in self.gameslots:
            g.game_event = []
            g.full = False
        self.recalculate_players()

    def print_problems(self, res):
        """
        This function prints out a list of problems encountered during a game.

        Args:
            res (dict): The `res` input parameter is a list of dicts containing
                game information and player data.

        """
        i = 0
        for r in res:
            print("PROBLEM: ", i)
            i += 1
            r["game"].log()
            for p in r["players"]:
                print(p.id)
            print()

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

    def get_days(self):
        """
        The function `get_days` takes an object of type `Self` as input and returns
        a dictionary where the keys are the day numbers and the values are lists
        of game slots that occur on those days.

        Returns:
            dict: The function `get_days` returns a dictionary with day numbers
            as keys and a list of slots for each day as values.

        """
        full_slots = [slot for slot in self.gameslots if slot.full == True]
        days = {}
        for slot in full_slots:
            if slot.day_number in days:
                days[slot.day_number].append(slot)
            else:
                days[slot.day_number] = [slot]
        return days

    def sort_out_preferences(self):
        """
        This function sorts out the preferences of a player by iterating through
        the games they have selected and checking if they can be swapped with other
        players who are available and willing to play at the same time slot.

        """
        days = self.get_days()
        for i in range(10):
            for key in days:
                sad_players = []
                for game in days[key]:
                    sad_players += game.get_sad_players_and_self()
                for pg in sad_players:
                    player = pg["player"]
                    for game in days[key]:
                        if (
                            game.full == True
                            and player.availability[game.timeslot_id] == AVAILABLE
                        ):
                            self.decide_how_to_swap(player, pg["game"], game)
                            break

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

    def no_players_overscheduled(self):
        """
        This function checks whether any of the players are overscheduled by
        comparing their game count to the maximum number of games they can play
        according to their rules.

        Returns:
            bool: The output returned by this function is `True`.

        """
        for player in self.players:
            if player.game_count > player.rules["max_games_total"]:
                return False
        return True

    def player_days_satisfied(self):
        """
        This function checks if all players have played at most the maximum number
        of games allowed per day as specified by their rules. It does this by
        iterating over each player's days and counting the number of games they
        have played on each day. If any player has played more than the maximum
        number of games on a given day , the function returns False .

        Returns:
            bool: Based on the code provided , the output of the `player_days_satisfied`
            function is `True` if all the players have satisfied their daily limit
            of games played .

        """
        for player in self.players:
            days = {}
            for day in player.days:
                if day in days:
                    days[day] += 1
                else:
                    days[day] = 1
            for key in days:
                if days[key] > player.rules["max_games_day"]:
                    return False
        return True

    def player_weeks_satisfied(self):
        """
        This function checks whether a list of players have satisfied their maximum
        games per week limitation for each week during the season. It iterates
        over each player and uses a dictionary to track the number of games played
        by that player per week. If any player has exceeded their maximum games
        per week for any week during the season then the function returns False
        indicating failure.

        Returns:
            bool: The output returned by the function `player_weeks_satisfied` is
            `True`.

        """
        for player in self.players:
            weeks = {}
            for w in player.weeks:
                if w in weeks:
                    weeks[w] += 1
                else:
                    weeks[w] = 1
            for key in weeks:
                if weeks[key] > player.rules["max_games_week"]:
                    return False
        return True

    def get_player_days_unsatisfied(self):
        """
        This function "get_player_days_unsatisfied" takes a list of players and
        their associated days as input and returns two lists: one containing players
        who have more games on a single day than their max_games_day rule allows;
        and another containing a dictionary mapping each player's id to the number
        of games they can play on the specified day.

        Returns:
            dict: The output returned by this function is a list of players (called
            "us") and a dictionary of game groups (called "bg") where each game
            group represents the games that a player has unsatisfied days for.

        """
        us = []
        bg = {}
        for player in self.players:
            days = {}
            for day in player.days:
                if day in days:
                    days[day] += 1
                else:
                    days[day] = 1
            for key in days:
                if days[key] > player.rules["max_games_day"]:
                    us.append(player)
                    bg[player.id] = self.find_games_on_day_with_player(player, key)
        return us, bg

    def find_games_on_day_with_player(self, player, day):
        """
        This function takes a `player` and a `day` as inputs and returns a list
        of all games on that day that the given player is participating In.

        Args:
            player (str): The `player` input parameter specifies the player whose
                presence is being searched for among the games on the specified day.
            day (int): The `day` parameter specifies which day to search for games
                on.

        Returns:
            list: The output returned by this function is a list of games that
            have the specified player and are scheduled on the specified day.

        """
        res = []
        for g in [g for g in self.gameslots if g.day_number == day]:
            if player in g.game_event:
                res.append(g)
        return res

    def log_player_days_unsatisfied(self):
        """
        This function logs the player IDs and their unsatisfied experiences
        (specifically start times) from a dictionary.

        """
        p, d = self.get_player_days_unsatisfied()
        for i in p:
            print(i.id)
            for k in d[i.id]:
                print(k.start_time)
            print()

    def get_gameslots_by_day(self, day_number):
        """
        This function retrieves a list of game slots that correspond to a specific
        day number.

        Args:
            day_number (int): The `day_number` input parameter specifies which
                day's game slots should be returned.

        Returns:
            list: The output returned by this function is a list of `Gameslot`
            objects that have a `day_number` attribute equal to the input `day_number`.

        """
        return [
            gameslot for gameslot in self.gameslots if gameslot.day_number == day_number
        ]

    def get_gameslots_by_week(self, week_number):
        """
        The given function `get_gameslots_by_week` takes a `week_number` parameter
        and returns a list of `Gameslot` objects that have the same week number
        as the given parameter.

        Args:
            week_number (int): The `week_number` input parameter specifies the
                week number for which to retrieve gameslots.

        Returns:
            list: The function `get_gameslots_by_week` returns a list of `GameSlot`
            objects that have a `week_number` equal to the given `week_number`.

        """
        return [
            gameslot
            for gameslot in self.gameslots
            if gameslot.week_number == week_number
        ]

    def log(self, dofilter=False):
        """
        The `log` function is a method of an object that has `players` and `gameslots`
        attributes.

        Args:
            dofilter (bool): The `dofilter` parameter is an optional argument
                passed to the `log()` function. It defaults to `False`.

        """
        for p in self.players:
            p.log(dofilter)
        for gs in self.gameslots:
            gs.log(dofilter)

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

    def get_average_failure_count(self):
        """
        This function calculates the average failure count for a list of players
        by subtracting the minimum games total for each player from their game
        count and then dividing the sum of these differences by the length of the
        player list.

        Returns:
            float: The output returned by this function would be `NaN`.

        """
        return sum(
            [abs(p.rules["min_games_total"] - p.game_count) for p in self.players]
        ) / len(self.players)

    def average_player_satisfaction(self):
        """
        This function calculates the average player satisfaction of a group of
        players by dividing the number of unsatisfied players by the total number
        of players.

        Returns:
            float: The output returned by the `average_player_satisfaction` function
            is `0`.

        """
        return len([p for p in self.players if p.satisfied is False]) / len(
            self.players
        )

    def get_average_and_max_player_luck(self):
        """
        This function calculates the average luck of players and returns a dictionary
        containing three values:
        	- "average" - the overall average luck of all players.
        	- "max" - the maximum luck of any single player.
        	- "variance" - a measure of how spread out the luck is among players
        (calculated as the average squared difference between each player's luck
        and the overall average).

        Returns:
            dict: The output returned by this function is a dictionary containing
            three items:
            
            	- "average": the overall average value of all players' luck scores
            	- "max": the maximum individual luck score among all players
            	- "variance": the variance of all players' luck scores

        """
        total = 0
        max_common = 0
        acc = 0
        values = []  # Store each individual value for variance calculation

        for p in self.players:
            res = p.get_most_common_player_and_count()
            for key in res:
                total += res[key]
                acc += 1
                values.append(res[key])
                if res[key] > max_common:
                    max_common = res[key]

        average = total / acc

        # Calculate variance
        variance = sum((x - average) ** 2 for x in values) / acc

        return {"average": average, "max": max_common, "variance": variance}

    def compare_basics(self, other):
        """
        This function compares two objects (self and other) by adding up their
        satisfied and captained player counts and returns a dictionary with the
        new score (self_score) and old score (other_score).

        Args:
            other (): In this function `compare_basics(self)`, `other` is the
                object being compared to `self`.

        Returns:
            dict: The output returned by this function is a dictionary with two
            keys: "new" and "old".

        """
        other_score = 0
        self_score = 0

        other_score += other.all_players_satisfied()
        other_score += other.all_players_captained_minimum()

        self_score += self.all_players_satisfied()
        self_score += self.all_players_captained_minimum()
        return {"new": self_score, "old": other_score}

    def log_unsatisfied_players(self):
        """
        The function `log_unsatisfied_players` iterates over the players attached
        to the game object and prints the ID and game count for each player who
        is not satisfied (i.e., whose `satisfied` attribute is `False`).

        """
        for p in self.players:
            if p.satisfied == False:
                print(p.id, p.game_count)

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



