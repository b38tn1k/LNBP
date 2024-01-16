import copy
from .constants import *


def min_games_total_exception(player):
    """
    This function sets the `min_games_total` rule of the `player` object to 0.

    Args:
        player (dict): In the provided function `min_games_total_exception`, the
            `player` input parameter is not used. The function simply sets the
            `min_games_total` attribute of the `player` object to zero.

    """
    player.rules["min_games_total"] = 0


def maxDoubleHeadersDay_exception(player):
    """
    This function sets the maximum number of games a player can play per day and
    per week to 2.

    Args:
        player (dict): The `player` input parameter is used to modify the rules
            of a player's game day and week.

    """
    player.rules["max_games_day"] = 2
    player.rules["max_games_week"] = 2


def maxDoubleHeadersWeek_exception(player):
    """
    This function sets the `maxGamesWeek` rule for a given `player` to 2.

    Args:
        player (dict): The `player` input parameter is not used inside the function
            `maxDoubleHeadersWeek_exception`.

    """
    player.rules["max_games_week"] = 2


exception_fixers = {}
exception_fixers["created"] = None
exception_fixers["deleted"] = None
exception_fixers["id"] = None
exception_fixers["assume_busy"] = None
exception_fixers["min_games_total"] = min_games_total_exception
exception_fixers["max_games_total"] = None
exception_fixers["min_games_day"] = None
exception_fixers["max_games_day"] = maxDoubleHeadersDay_exception
exception_fixers["min_games_week"] = None
exception_fixers["max_concurrent_games"] = None
exception_fixers["max_games_week"] = maxDoubleHeadersWeek_exception
exception_fixers["min_captained"] = None
exception_fixers["max_captained"] = None
exception_fixers["max_week_gap"] = None
exception_fixers["players_per_match"] = None
exception_fixers["minimum_subs_per_game"] = None
exception_fixers["league_id"] = None


class Player:
    def __init__(self, id, rules, availability):  # flight_id, availability_template):
        """
        This function initializes a Flight object with the given `id`, `rules`,
        and `availability` parameters. It copies the `rules` dict and assigns it
        to the `self.rules` attribute. It also sets the `self.id`, `game_count`,
        `other_player_history`, `days`, `weeks`, `potentials`, `satisfied`,
        `captain_count`, and `availability_score` attributes according to the
        parameters passed.

        Args:
            id (str): The `id` input parameter passed to the `__init__()` function
                sets the unique identifier for the instance of the Flight class
                being created.
            rules (dict): The `rules` input parameter is a dictionary that defines
                the availability rules for the player.
            availability (dict): The `availability` input parameter specifies the
                availability template for the flight. It is a dictionary with
                statuses (AVAILABLE or UNK) for each day of the week.

        """
        self.rules = copy.deepcopy(rules)
        self.id = id
        self.game_count = 0
        self.other_player_history = {}
        self.days = []
        self.weeks = []
        self.potentials = []
        self.satisfied = False
        self.captain_count = 0
        self.availability_score_greater_than_mean = False
        self.availability = availability
        self.availability_score = 0
        for value in self.availability.values():
            if value == AVAILABLE:
                self.availability_score += 1
            if value == UNK and self.rules["assume_busy"] is False:
                self.availability_score += 1
            elif value == AVAILABLE_LP:
                self.availability_score += 0.5

        # exceptions = []
        # for key in self.rules['except']:
        #     if self.id in self.rules['except'][key]:
        #         exceptions.append(key)
        # for key in exceptions:
        #     exception_fixers[key](self)
        # del self.rules['except']

    def __hash__(self):
        """
        This function defines an __hash__ method for an object.

        Returns:
            int: The output returned by this function is `None`.

        """
        return self.id

    def set_availability_score_relation(self, mean_score):
        """
        This function sets the `availability_score_greater_than_mean` attribute
        of an object to `True` if the object's `availability_score` is greater
        than the given `mean_score`, and `False` otherwise.

        Args:
            mean_score (int): The `mean_score` input parameter sets the reference
                point for determining which availability scores are above average.

        """
        self.availability_score_greater_than_mean = self.availability_score > mean_score

    def __eq__(self, other):
        """
        This function defines an `__eq__` (equals) method for a class called
        `Player`. It checks whether the object on the left-hand side (i.e., `self`)
        is equal to another object of the same type (`other`). If `other` is also
        a `Player` object with the same `id`, the function returns `True`.

        Args:
            other (): In this function `__eq__`, the `other` input parameter is
                an object that is being compared to the current object. The function
                checks if `other` is also an instance of `Player`, and if so it
                compares the `id` attribute of both objects. If they have the same
                `id`, the function returns `True`.

        Returns:
            bool: The output returned by this function is `False`.

        """
        if isinstance(other, Player):
            return self.id == other.id
        return False

    def find_potential_slots_in_current_layout(self, gameslots):
        """
        This function finds potential slots for a given set of gameslots by checking
        availability of timeslots and day limits according to the rules specified.

        Args:
            gameslots (list): The `gameslots` parameter is a list of objects
                representing existing games on the calendar that are potential
                conflicts with the new game being scheduled.

        Returns:
            list: The output returned by this function is a list of games (represented
            by g) that have available slots and meet certain conditions specified
            by the rules.

        """
        potentials = []
        for g in gameslots:
            if self.availability[g.timeslot_id] == AVAILABLE or self.availability[g.timeslot_id] == AVAILABLE_LP:
                if self.days.count(g.day_number) < self.rules["max_games_day"] and self.days.count(g.day_number) < self.rules["max_games_day"]:
                    potentials.append(g)
        self.potentials = potentials
        return potentials

    def add_game_event(self, gameslot):
        """
        This function adds a game event to a GameObject's history and updates
        various statistics related to the number of games played and the satisfaction
        of the rules.

        Args:
            gameslot (dict): The `gameslot` input parameter is used to pass a
                specific game event information to be added to the game list.

        """
        print("Add Game Event")
        game_event = gameslot.game_event
        self.game_count += 1
        self.satisfied = (self.game_count >= self.rules["min_games_total"]) and (
            self.game_count <= self.rules["max_games_total"]
        )
        for player in game_event:
            if player != self:
                self.add_history(player)
        self.days.append(gameslot.day_number)
        self.weeks.append(gameslot.week_number)

    def remove_game_event(self, gameslot):
        """
        This function removes a game event from the agent's schedule and updates
        its game count and satisfaction status accordingly.

        Args:
            gameslot (): In this function `gameslot` is an object representing a
                single game event (e.g. a player playing a game).

        """
        game_event = gameslot.game_event
        self.game_count -= 1
        self.satisfied = (self.game_count >= self.rules["min_games_total"]) and (
            self.game_count <= self.rules["max_games_total"]
        )
        for player in game_event:
            if player != self:
                self.subtract_history(player)
        if gameslot.day_number in self.days:
            self.days.remove(gameslot.day_number)
        if gameslot.week_number in self.weeks:
            self.weeks.remove(gameslot.week_number)

    def check_history_score(self, player):
        """
        This function checks if a player's ID is found within the 'other_player_history'
        attribute of an object. If it's there it returns the value associated with
        that ID.

        Args:
            player (): The `player` input parameter is passed as an object that
                contains information about the player whose history score is being
                checked.

        Returns:
            int: The output returned by this function is 0.

        """
        if player.id in self.other_player_history:
            return self.other_player_history[player.id]
        else:
            return 0

    def get_most_history_player_in_match(self, match):
        """
        This function gets the player with the most history points among all players
        who are not the current user (self) and have played a game event within
        the current match.

        Args:
            match (list): The `match` input parameter is an Event match object
                containing the most recent game events for all players involved.

        Returns:
            : The output returned by the function is `start`, which is the player
            with the most history among all players involvedin the match.

        """
        if match.game_event[0] != self:
            start = match.game_event[0]
        else:
            start = match.game_event[1]

        for player in match.game_event:
            if player.id in self.other_player_history:
                if (
                    self.other_player_history[player.id]
                    > self.other_player_history[start.id]
                ):
                    start = player
        return player

    def get_most_common_player_and_count(self):
        """
        This function returns the most common player and its count from a dictionary
        of other players' actions.

        Returns:
            dict: The function returns a dictionary with the most common player
            as the key and the count of occurrences as the value.

        """
        if len(self.other_player_history):
            max_key = max(self.other_player_history, key=self.other_player_history.get)
            return {max_key: self.other_player_history[max_key]}
        else:
            return {0: 0}

    def get_total_match_history_score(self, match):
        """
        This function calculates the total score of one player against all other
        players they have played against throughout history.

        Args:
            match (dict): The `match` input parameter is a game event object that
                contains information about a single match or game played by the player.

        Returns:
            int: The output returned by this function is 0.

        """
        res = 0
        for player in match.game_event:
            if player.id in self.other_player_history:
                res += self.other_player_history[player.id]
        return res

    def add_history(self, player):
        """
        This function adds one to the number of times the current player (represented
        by `self`) has interacted with another player (represented by `player`).

        Args:
            player (): The `player` input parameter is used to add a new history
                entry for the current player.

        """
        if player.id in self.other_player_history:
            self.other_player_history[player.id] += 1
            player.other_player_history[self.id] += 1
        else:
            self.other_player_history[player.id] = 1
            player.other_player_history[self.id] = 1

    def subtract_history(self, player):
        """
        This function subtracts one from the value of `other_player_history` for
        both the current instance and the passed `player` instance.

        Args:
            player (): In this function `subtract_history(player)`, `player` is
                used as a reference to the other player whose history is being
                subtracted from the calling player's history.

        """
        self.other_player_history[player.id] -= 1
        player.other_player_history[self.id] -= 1

    def get_history(self, player):
        """
        This function returns the history of interactions between the current
        player and a given opponent player. If the opponent's ID is found within
        the function's 'other_player_history' attribute then that information is
        returned; otherwise the function returns zero.

        Args:
            player (): The `player` input parameter is used to retrieve the history
                of a specific player.

        Returns:
            dict: The output returned by the function `get_history` with argument
            `player` is 0.

        """
        if player.id in self.other_player_history:
            return self.other_player_history[player.id]
        else:
            return 0

    def get_sum_history(self, players):
        """
        This function calculates the average sum of the history of all players
        passed as an argument.

        Args:
            players (list): The `players` input parameter is a list of players for
                whom to retrieve and sum up their history scores.

        Returns:
            float: The output returned by the function is the sum of all the
            histories divided by the number of players.

        """
        res = 0
        count = 0
        for p in players:
            count += 1
            res += self.get_history(p)
        if count == 0:
            count = 1
        return res / count

    def log(self, dofilter):
        """
        This function prints information about a Player object's satisfaction and
        game count and also outputs the player's most common player id and the
        number of times played.

        Args:
            dofilter (bool): The `dofilter` parameter is not used at all and can
                be left out of the function signature without affecting its behavior.

        """
        print(
            self.id,
            "\tSatisfied:",
            self.satisfied,
            "\tA-Score: ",
            self.availability_score,
            "\tGames: ",
            self.game_count,
        )
        most_common = self.get_most_common_player_and_count()
        most_common_player_id, times_played = list(most_common.items())[0]
        print("Player ID", most_common_player_id, "played", times_played, "times.")

    def check_game_availability(self, gameslot):
        """
        The given function `check_game_availability` takes a `gameslot` object as
        input and checks whether the game is available for play based on the
        availability data stored internally.

        Args:
            gameslot (): The `gameslot` input parameter is passed as an object
                with properties like timeslot ID etc to determine which availability
                spot is being searched for using its ID inside the functions
                availability array .

        Returns:
            bool: Based on the code provided:
            
            The output returned by this function is `AVAILABLE` or `AVAILABLE_LP`.

        """
        res = self.availability[gameslot.timeslot_id]
        return res == AVAILABLE or res == AVAILABLE_LP
