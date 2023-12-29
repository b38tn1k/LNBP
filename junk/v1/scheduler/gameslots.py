import pytz
from datetime import datetime, timedelta
import statistics
from random import shuffle, choice, seed
from .utils import *


def findAllGameSlots(flight, rules):
    """
    This function findAllGameSlots finds available game slots for a given flight
    of basketball games based on the rules provided. It iterates through the
    timeslots of the flight and creates a list of GameSlot objects that have no
    colliding events.

    Args:
        flight (): The `flight` input parameter is an instance of the `Flight`
            class and contains information about the available courts and time
            slots for a particular flight.
        rules (dict): The `rules` input parameter is a dictionary of rules that
            define how to generate game slots.

    Returns:
        dict: The function `findAllGameSlots` returns two things:
        
        1/ A dictionary `template` where each key is a timeslot ID and the
        corresponding value is -1 if there is no conflict for that timeslot.
        2/ A list `res` of `GameSlot` objects representing all possible game slots.

    """
    res = []
    template = {}
    for timeslot in flight.timeslots:
        for court in timeslot.courts:
            colliding_events = court.get_colliding_events(timeslot, flight.id)
            if len(colliding_events) == 0:
                gameSlot = GameSlot(timeslot, court, rules)
                gameSlot.temp_players
                res.append(gameSlot)
                template[timeslot.id] = -1
    for event in flight.get_event_objects():
        for ts in res:
            if ts.timeslot_id == event.timeslot.id and ts.court_id == event.court.id:
                ts.event_obj = event
                for player in event.get_player_ids():
                    ts.temp_players.append(player)
    return template, res

def days_and_weeks_since_y2k_lol(dt, tz=None):
    """
    This function takes a `datetime` object `dt` and optionally a time zone (`tz`),
    and returns the number of days and weeks since December 31st 1999 (Y2K) based
    on the given datetime and time zone.

    Args:
        dt (): The `dt` input parameter is the datetime object for which to calculate
            the number of days and weeks since Y2K.
        tz (str): The `tz` input parameter is used to specify a timezone string
            to localize the Y2K timestamp (`y2k`) to the specific timezone if provided.

    Returns:
        int: The output returned by this function is a tuple containing two values:
        `days` and `weeks`.

    """
    y2k = datetime(2000, 1, 1)  # Start from Y2K
    if tz is not None:
        timezone = pytz.timezone(tz)
        y2k = timezone.localize(y2k)  # Localize to the specific timezone if provided

    delta = dt - y2k  # Calculate the timedelta from Y2K to the given datetime
    days = delta.days  # Get the number of days from the timedelta
    weeks = days // 7
    return days, weeks

class GameSlot:
    def __init__(self, timeslot, court, rules):
        """
        This function initizes a class for managing basketball game scheduling
        information. It sets class attributes with values from the input parameters
        "timeslot", "court", and "rules".

        Args:
            timeslot (): The `timeslot` input parameter specifies the time slot
                for which the Game instance is being created.
            court (): The `court` input parameter is used to pass a reference to
                an instance of the `Court` class as a parameter to the `__init__`
                method.
            rules (dict): The `rules` input parameter defines the rules for the
                timeslot's game session.

        """
        self.rules = rules
        self.timeslot_obj = timeslot
        self.start_time = timeslot.start_time
        self.court_obj = court
        self.timeslot_id = timeslot.id
        self.court_id = court.id
        self.court_name = court.court_name
        self.day_number, self.week_number = days_and_weeks_since_y2k_lol(
            self.start_time
        )
        self.game_event = []
        self.temp_players = []
        self.full = False
        self.captain = None
        self.good_availability = True
        self.event_obj = None

    def __hash__(self):
        """
        This function defines an __hash__ method for an object.

        Returns:
            int: The output returned by this function is the sum of `self.timeslot_id`
            and `self.court_id`.

        """
        return self.timeslot_id + self.court_id

    def duplicate(self):
        """
        This function duplicates an object of a class that has attributes
        `timeslot_obj`, `court_obj`, and `rules`.

        Returns:
            : The function "duplicate" returns an object of the same class as the
            original object (i.e., itself).

        """
        return type(self)(self.timeslot_obj, self.court_obj, self.rules)

    def copy_with_events(self):
        """
        This function copies an instance of a class (`self`) and adds the game
        events from `self` to a new instance of the same class (`gs`).

        Returns:
            list: The function "copy_with_events" returns a new instance of the
            class "GameState" with all the attributes of the original object plus
            the list of game events.

        """
        gs = type(self)(self.timeslot_obj, self.court_obj, self.rules)
        for p in self.game_event:
            gs.game_event.append(p)
        gs.full = self.full
        return gs

    def log(self, dofilter=True):
        """
        This function logs information about a game event to the console.

        Args:
            dofilter (bool): The `dofilter` parameter is an optional argument that
                is set to `True` by default. When `dofilter` is `True`, the function
                will only print if the `game_event` list is not empty.

        """
        if dofilter and len(self.game_event) == 0:
            return
        else:
            print("Time Slot: ", self.timeslot_id, "\tCourt: ", self.court_id)
            print("Day #: ", self.day_number, "\tWeek #: ", self.week_number)
            players = ""
            for player in self.game_event:
                players += player.player_name + " "
            print("Players: ", players)
            print("Homogenity Score: ", self.get_total_availability_score())
            print("\n")

    def player_can_be_added(self, player):
        # hasCapacity = not (self.full)
        """
        This function checks whether a player can be added to a game event based
        on their availability and the game rules.

        Args:
            player (): The `player` input parameter passed to the `player_can_be_added()`
                function represents the player object that the function is supposed
                to check if can be added to the event or not.

        Returns:
            bool: The output returned by this function is `False`.

        """
        if self.full:
            return False
        if player in self.game_event:
            return False
        # isNew = not (player in self.game_event)
        isAvailable = (player.availability[self.timeslot_id] == AVAILABLE) or (
            player.availability[self.timeslot_id] == AVAILABLE_LP
            and len(self.game_event) >= self.rules["playersPerMatch"] - 2
        )
        dayCountOk = player.days.count(self.day_number) < player.rules["maxGamesDay"]
        weekCountOk = player.days.count(self.day_number) < player.rules["maxGamesWeek"]
        return isAvailable and dayCountOk and weekCountOk

    def hypothetically_player_can_be_added(self, player):
        """
        This function checks if a given player can be added to the current game
        slot (based on availability and max games per day/week restrictions) and
        returns True if they can be added and False otherwise.

        Args:
            player (): The `player` input parameter passes a Player object as an
                argument to the function.

        Returns:
            bool: The output returned by the function is a boolean value indicating
            whether the player can be added to the game or not.

        """
        isNew = not (player in self.game_event)
        isAvailable = (player.availability[self.timeslot_id] == AVAILABLE) or (
            player.availability[self.timeslot_id] == AVAILABLE_LP
        )
        dayCountOk = player.days.count(self.day_number) < player.rules["maxGamesDay"]
        weekCountOk = player.days.count(self.day_number) < player.rules["maxGamesWeek"]
        return isNew and isAvailable and dayCountOk and weekCountOk

    def __eq__(self, other):
        """
        This function checks whether two objects are equal by comparing their
        `timeslot_id` attributes.

        Args:
            other (): In the provided code snippet:
                
                The `other` input parameter is used to compare the current object
                (`self`) with another object of the same class (`GameSlot`).

        Returns:
            int: Based on the code provided:
            
            The output returned by this function would be `False`, because the
            comparison with `other` object will only return true if it is also an
            instance of `GameSlot` class and if the both slots have the same `timeslot_id`.

        """
        if isinstance(other, GameSlot):
            c1 = self.timeslot_id = other.timeslot_id
            c2 = self.timeslot_id = other.timeslot_id
            return c1 and c2
        return False

    def add_player_to_match(self, player):
        """
        This function adds a player to a match and manages the player list
        accordingly. It checks if the player can be added and if the maximum number
        of players per match has been reached.

        Args:
            player (): The `player` input parameter is passed as an argument to
                the `add_game_event` method of the `player` object.

        """
        if self.player_can_be_added(player):
            player.add_game_event(self)
            self.game_event.append(player)
            if len(self.game_event) == self.rules["playersPerMatch"]:
                self.full = True
            self.captain = choice(self.game_event)

    def force_player_to_match(self, player):
        """
        This function forces a player to participatein a match and sets the full
        flag to true when the number of players who have joined the event equals
        the number of players required per match according to the rules.

        Args:
            player (): The `player` input parameter forces the player to be added
                as an event for the current match.

        """
        player.add_game_event(self)
        self.game_event.append(player)
        if len(self.game_event) == self.rules["playersPerMatch"]:
            self.full = True

    def get_most_available_player(self):
        """
        This function returns the player with the highest availability score among
        all players available to play. It scans the list of players (self.game_event)
        starting from the first player (lead) and compares their availability
        scores. If a player has a higher availability score than the current lead
        player. The lead player is reassigned to that player.

        Returns:
            : The function `get_most_available_player` takes an instance of a class
            `GameEvent` as input and returns the most available player from the
            list of players.
            
            The output returned by this function is the most available player found
            among the list of players.

        """
        lead = self.game_event[0]
        for player in self.game_event[1:]:
            if player.availability_score > lead.availability_score:
                lead = player
        return lead

    def get_most_served_player(self):
        """
        This function returns the player who has been served most frequently (i.e.,
        played the most games) based on the list of players and their corresponding
        game counts stored within the `self.game_event` list.

        Returns:
            : The output returned by this function is the "most served player"
            object from the list of players.

        """
        lead = self.game_event[0]
        for player in self.game_event[1:]:
            if player.game_count > lead.game_count:
                lead = player
        return lead

    def get_swap_candidate_player(self):
        # Compute the median availability score
        """
        This function computes the median availability score of players and selects
        the player with the highest game count among those above the median as the
        best candidate to be paired.

        Returns:
            : The output returned by this function is `above_median_availability_players[0]`.

        """
        median_availability_score = statistics.median(
            player.availability_score for player in self.game_event
        )
        # Filter the players with above median availability scores
        above_median_availability_players = [
            player
            for player in self.game_event
            if player.availability_score >= median_availability_score
        ]
        # Initialize the best candidate with the first player
        best_candidate = above_median_availability_players[0]
        # Go through the rest of the players, updating the best candidate as needed
        for player in above_median_availability_players[1:]:
            if player.game_count < best_candidate.game_count:
                best_candidate = player
        return best_candidate

    def swap_in(self, player, filter=True):
        """
        This function swaps out a player from a match if they have reached the
        minimum number of games required by their rules.

        Args:
            player (): The `player` input parameter is used to specify the player
                that should be swapped into the match.
            filter (bool): The `filter` parameter controls whether to only swap
                out a player if their game count is less than the minimum games
                total and less than the current player's game count.

        Returns:
            : The function "swap_in" returns the "swap_out" player.

        """
        if player in self.game_event:
            return player
        swap_out = self.get_swap_candidate_player()
        if (
            filter
            and swap_out.game_count < player.rules["minGamesTotal"]
            and swap_out.game_count < player.game_count
        ):
            return player
        self.remove_player_from_match(swap_out)
        self.add_player_to_match(player)
        return swap_out

    def get_total_availability_score(self):
        """
        This function calculates the total availability score of all players on
        the game event list.

        Returns:
            int: The output returned by this function is 0.

        """
        tas = 0
        for player in self.game_event:
            tas += player.availability_score
        return tas

    def get_player_match_history_score(self):
        """
        This function retrieves the total match history score for each player In
        a game event and returns a list of all the players' scores.

        Returns:
            list: Based on the given code snippet:
            
            The function `get_player_match_history_score` takes no arguments and
            returns a list of integers (`scores`).
            
            The function iterates over each player object found within the
            `self.game_event` list and calls the `get_total_match_history_score`
            method for each player.

        """
        scores = []
        for player in self.game_event:
            scores.append(player.get_total_match_history_score(self))
        return scores

    def is_building_already(self):
        """
        The `is_building_already` function checks whether the current player has
        already built a building during their turn by checking if there are any
        events for that turn and if the player is not full (i.e., if they can still
        add another event).

        Returns:
            bool: Based on the given code snippet:
            
            The output returned by the `is_building_already` function is `False`.

        """
        return len(self.game_event) > 0 and not (self.full)

    def remove_player_from_match(self, player):
        """
        This function removes a player from the game event associated with the
        instance (presumably a Game or Match object), and updates the full status
        of the game.

        Args:
            player (): The `player` input parameter is used to specify the player
                object that needs to be removed from the match.

        """
        player.remove_game_event(self)
        if player in self.game_event:
            self.game_event.remove(player)
        self.full = False

    def all_players_satisfy_min_games(self):
        """
        This function checks if all players have played more games than their
        "minGamesTotal" value set on their rules.

        Returns:
            bool: The function `all_players_satisfy_min_games()` returns `True`.

        """
        return all(
            player.game_count > player.rules["minGamesTotal"]
            for player in self.game_event
        )

    def destruct(self):
        """
        This function destructs (or removes) the objects that have registered game
        events with the current object.

        """
        for player in self.game_event:
            player.remove_game_event(self)
        self.game_event = []
        self.full = False

    def self_destruct_if_unneccessary(self):
        """
        This function will call the `destruct` method on itself if all players
        satisfy the minimum number of games required.

        """
        if self.all_players_satisfy_min_games():
            self.destruct()

    def self_destruct_if_incomplete(self):
        """
        This function will cause the object to destruct itself if it is not fully
        initialized (i.e., if `self.full` is falsey).

        """
        if not (self.full):
            self.destruct()

    def get_players_available_to_swap(self, other_match):
        """
        This function returns a list of players who are available to be swapped
        from the current match (represented by `self`) to another match (represented
        by `other_match`).

        Args:
            other_match (): The `other_match` parameter is used to check if a
                player from the current match can be added to the other match
                without violating any team's minimum player requirement.

        Returns:
            list: The function "get_players_available_to_swap" returns a list of
            players.

        """
        available_players = []
        for player in self.game_event:
            if other_match.hypothetically_player_can_be_added(player):
                available_players.append(player)
        return available_players

    def logps(self, ps):
        """
        The function `logps` takes a list of dictionaries `ps` where each dictionary
        represents a player and prints out the name of each player.

        Args:
            ps (list): The `ps` input parameter is a list of objects (presumably
                player objects) that the function iterates over and prints the
                `player_name` attribute of each object.

        """
        for p in ps:
            print(p.player_name)

    def get_inverse_players(self, players):
        """
        The given function `get_inverse_players` takes a list of players and returns
        a list of all players that are not present among the passed players.

        Args:
            players (list): The `players` input parameter is a list of players
                that are not to be included from `self.game_event` when creating
                the list of inverse players.

        Returns:
            list: The function takes a list of players `players` as input and
            returns a list of players that are not present inside the list `players`.

        """
        inverse = []
        for p in self.game_event:
            if not (p in players):
                inverse.append(p)
        return inverse

    def compare_histories_stay(self, group, stay, go):
        """
        This function compares the histories of players' stays and goes by computing
        their individual scores and storing them as a list of dictionaries.

        Args:
            group (list): The `group` input parameter is a list of players that
                are being compared for their histories.
            stay (list): In this function `compare_histories_stay`, the `stay`
                input parameter is used to calculate the score for each player
                when they choose to stay with their current hand rather than drawing
                a new one.
            go (dict): The `go` input parameter is passed as a dictionary of history
                items for each player and its score to compare with the "stay"
                score from the same player's history.

        Returns:
            dict: The function `compare_histories_stay` returns a list of dictionaries
            each containing three scores: "player", "stay_score", and "go_score".

        """
        scores = []  # List to store scores for all players
        for p in group:
            stay_or_go = {}  # Individual dictionary for each player's scores
            stay_or_go["player"] = p
            s = p.get_sum_history(stay)
            g = p.get_sum_history(go)
            stay_or_go["stay_score"] = s
            stay_or_go["go_score"] = g
            scores.append(stay_or_go)
        return scores

    def try_exchange(self, other_match, try_hard=False):
        """
        This function tries to exchange two players between two different matches
        to improve the overall score of both matches.

        Args:
            other_match (): The `other_match` input parameter is a Match object
                that is used to find potential player swaps with.
            try_hard (bool): The `try_hard` input parameter is used to indicate
                whether to consider players with high historical scores as potentially
                good swaps even if they have fewer matches than other players.

        Returns:
            bool: The output of this function is a boolean value indicating whether
            two player exchanges were successful (True) or not (False).

        """
        owned_players_can_go = self.get_players_available_to_swap(other_match)
        other_players_can_go = other_match.get_players_available_to_swap(self)
        if len(owned_players_can_go) > 0 and len(other_players_can_go) > 0:
            owned_players_must_stay = self.get_inverse_players(owned_players_can_go)
            other_players_must_stay = other_match.get_inverse_players(
                other_players_can_go
            )
            own_players_swap_scores = self.compare_histories_stay(
                owned_players_can_go, owned_players_must_stay, other_players_must_stay
            )
            other_players_swap_scores = other_match.compare_histories_stay(
                other_players_can_go, other_players_must_stay, owned_players_must_stay
            )
            best_own_player = max(
                own_players_swap_scores, key=lambda x: x["stay_score"]
            )["player"]
            best_other_player = min(
                other_players_swap_scores, key=lambda x: x["go_score"]
            )["player"]
            # double check
            new_possible_own = self.get_inverse_players([best_own_player])
            new_possible_other = other_match.get_inverse_players([best_other_player])
            good_for_own = (
                best_own_player.get_sum_history(new_possible_own)
                > best_own_player.get_sum_history(new_possible_other)
                or try_hard
            )
            good_for_other = (
                best_other_player.get_sum_history(new_possible_other)
                > best_other_player.get_sum_history(new_possible_own)
                or try_hard
            )
            if good_for_own and good_for_other:
                other_match.remove_player_from_match(best_other_player)
                self.remove_player_from_match(best_own_player)
                other_match.add_player_to_match(best_own_player)
                self.add_player_to_match(best_other_player)
                return True
        return False
        # check if players are available for the other match
        # check if other match players are available for this match
        # check if other match contains players in history greater than players in history in current match
        # do the same for this one
        # swap

    def get_sad_players_and_self(self):
        """
        This function retrieves a list of "sad" players (i.e., players who are
        available to play during a specific timeslot) and returns it.

        Returns:
            dict: The output returned by this function is `[]`, an empty list of
            dictionaries.

        """
        sad_players = []
        for player in self.game_event:
            if player.availability[self.timeslot_id] == AVAILABLE_LP:
                pg = {}
                pg["game"] = self
                pg["player"] = player
                sad_players.append(pg)
        return sad_players

    def calculate_history_delta(self, other_player, ignore_player):
        """
        This function calculates the delta score between two players (self and
        other_player) by iterating through each game event and calculating the
        score difference between the two players for that event.

        Args:
            other_player (): The `other_player` parameter is passed as an optional
                parameter to `calculate_history_ delta()`.
            ignore_player (): The `ignore_player` input parameter is used to exclude
                that player from the calculation of the history delta.

        Returns:
            int: The output returned by this function is 0.

        """
        history_delta = 0
        for p in self.game_event:
            if p != ignore_player:
                history_delta += other_player.check_history_score(p)
        return history_delta
