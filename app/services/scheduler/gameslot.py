import statistics
from random import choice
from .constants import *

class GameSlot:
    def __init__(self, tid, fid, y2k_counter, rules):
        """
        This function defines an object called `__init__` and sets its attributes
        as follows:
        	- `rules`: a list of rules
        	- `timeslot_id`: an integer identifying the timeslot
        	- `facility_id`: an integer identifying the facility
        	- `day_number`: an integer representing the day number (0-based)
        	- `week_number`: an integer representing the week number (0-based)
        	- `game_event`: a list of game events
        	- `temp_players`: a list of temporary players
        	- `full`: a boolean indicating whether the facility is full or not
        	- `captain`: an object representing the captain of the team
        	- `good_availability`: a boolean indicating whether there is good
        availability of players or not
        	- `event_obj`: an object representing the event
        In other words.

        Args:
            tid (int): The `tid` input parameter is used to identify the specific
                timeslot for which this GameEvent object represents scheduling information.
            fid (int): The `fid` input parameter specifies the facility ID for
                which the scheduling rules are being applied.
            y2k_counter (dict): The `y2k_counter` input parameter passed to the
                `__init__()` function is used to initialize the object's `day_number`
                and `week_number` attributes.
            rules (list): The `rules` input parameter is a list of rules that
                define how the scheduling algorithm should handle the scheduling
                of games and events.

        """
        self.rules = rules
        self.timeslot_id = tid
        self.facility_id = fid
        self.day_number = y2k_counter['days']
        self.week_number = y2k_counter['weeks']
        self.game_event = []
        self.temp_players = []
        self.full = False
        self.captain = None
        self.good_availability = True
        self.event_obj = None
        self.availability_score = 0

    def __hash__(self):
        """
        This function defines an Object-Oriented Programming (OOP) `__hash__()`
        method for a custom object class.

        Returns:
            int: The output returned by this function is the sum of `self.timeslot_id`
            and `self.facility_id`.

        """
        return self.timeslot_id + self.facility_id

    def duplicate(self):
        """
        The given function `duplicate` creates a copy of the current instance of
        the class by supplying the same attributes (`timeslot_id`, `days`, `weeks`,
        and `rules`) to the constructor of the same class.

        Returns:
            : The output of the `duplicate` function is a new `Timeslot` object
            with the same attributes as the original ` Timeslot` object: `timeslot_id`,
            `days`, `weeks`, and `rules`.

        """
        return type(self)(self.timeslot_id, {'days': self.day_number, 'weeks': self.week_number}, self.rules)

    def copy_with_events(self):
        """
        This function creates a duplicate of the object and appends all the game
        events from the original object to the duplicate.

        Returns:
            list: The output returned by the `copy_with_events` function is a deep
            copy of the original `GameState` object with all game events appended
            to the new object.

        """
        gs = self.duplicate()
        for p in self.game_event:
            gs.game_event.append(p)
        gs.full = self.full
        return gs
    
    def has_player_with_lp(self):
        res = False
        for p in self.game_event:
            if p.availability[self.timeslot_id] == AVAILABLE_LP:
                res = True
        return res


    def log(self, dofilter=True):
        """
        This function logs information about the current time slot and the players
        available for a game event to the console.

        Args:
            dofilter (bool): The `dofilter` input parameter is an optional argument
                that specifies whether to filter out empty lists of game events
                before printing them.

        """
        if dofilter and len(self.game_event) == 0:
            return
        else:
            print("Time Slot: ", self.timeslot_id, "\tCourt: ", self.facility_id)
            print("Day #: ", self.day_number, "\tWeek #: ", self.week_number)
            players = ""
            for player in self.game_event:
                players += player.id + " "
            print("Players: ", players)
            print("Homogenity Score: ", self.get_total_availability_score())
            print("\n")

    def player_can_be_added(self, player):
        # hasCapacity = not (self.full)
        """
        This function checks if a player can be added to a game based on their
        availability and limitations set by the player's rules and the current
        game event.

        Args:
            player (dict): The `player` input parameter is a game event participant
                object that determines if they can be added to the game event or
                not based on availability and constraints specified by their rules.

        Returns:
            bool: The output returned by this function is `True` or `False`,
            depending on whether the given `player` can be added to the game or not.

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
        This function checks whether a given player can be added to the current
        game session based on various conditions such as availability (both standard
        and Lightweight Pools), maximum number of games per day and per week
        according to their defined rules.

        Args:
            player (): The `player` input parameter passed to the
                `hypothetically_player_can_be_added()` function takes a player
                object as an argument and checks if that specific player can be
                added to the game event based on their availability and other
                conditions specified within the function's logic.

        Returns:
            bool: The output returned by the function is `False`.

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
        This function defines an equality comparison method (`__eq__`) for an
        object of type `GameSlot`.

        Args:
            other (): The `other` input parameter is used to compare the current
                object with another object of the same type (in this case `GameSlot`).

        Returns:
            bool: The function returns `True` if the object is instances of
            `GameSlot`, otherwise it returns `False`.

        """
        if isinstance(other, GameSlot):
            c1 = self.timeslot_id = other.timeslot_id
            c2 = self.timeslot_id = other.timeslot_id
            return c1 and c2
        return False

    def add_player_to_match(self, player):
        """
        This function adds a player to a match and checks if the maximum number
        of players has been reached.

        Args:
            player (): The `player` input parameter is passed to the function as
                a player object and is used to determine if the current player can
                be added to the match.

        """
        if self.player_can_be_added(player):
            player.add_game_event(self)
            self.game_event.append(player)
            if len(self.game_event) == self.rules["playersPerMatch"]:
                self.full = True
            self.captain = choice(self.game_event)

    def force_player_to_match(self, player):
        """
        This function forces a player to participate In a game event and adds them
        to a list of players for that match.

        Args:
            player (): The `player` input parameter forces the game to assign a
                specific player to match.

        """
        # print("Force Player To Match")
        player.add_game_event(self)
        self.game_event.append(player)
        if len(self.game_event) == self.rules["players_per_match"]:
            self.full = True

    def get_most_available_player(self):
        """
        This function retrieves the player with the highest availability score
        among all players except for the first one (lead) and returns that player
        as the most available player.

        Returns:
            : The output returned by the function `get_most_available_player` is
            the player object with the highest availability score among all players
            except the first one (i.e., `self.game_event[0]`).

        """
        lead = self.game_event[0]
        for player in self.game_event[1:]:
            if player.availability_score > lead.availability_score:
                lead = player
        return lead

    def get_most_served_player(self):
        """
        This function finds the player who has played the most games so far by
        comparing their game count to the current leader's game count.

        Returns:
            : The function `get_most_served_player` returns the player with the
            highest game count among all players.

        """
        lead = self.game_event[0]
        for player in self.game_event[1:]:
            if player.game_count > lead.game_count:
                lead = player
        return lead

    def get_swap_candidate_player(self):
        # Compute the median availability score
        """
        This function finds the player with the highest availability score among
        those who have played at least one game with the given game event. It first
        computes the median availability score of all players and then filters out
        players with below-median scores.

        Returns:
            : The output returned by this function is "best_candidate", which is
            the player with the highest game count among the players with availability
            scores above the median availability score.

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
        This function "swaps" one player with another player of a similar skill
        level and game count.

        Args:
            player (): The `player` input parameter specifies the player to be
                swapped into the match.
            filter (bool): The `filter` input parameter is used to determine whether
                the swap candidate player should be accepted based on their minimum
                games total.

        Returns:
            : The output returned by this function is `swap_out`.

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
        This function calculates the total availability score of all players (object
        of 'player') contained within a game_event attribute.

        Returns:
            int: The output returned by this function is 0.

        """
        tas = 0
        for player in self.game_event:
            tas += player.availability_score
        return tas

    def get_player_match_history_score(self):
        """
        This function retrieves the total match history score for each player from
        the game event list and returns a list of these scores.

        Returns:
            list: The output returned by this function is a list of strings called
            `scores`.

        """
        scores = []
        for player in self.game_event:
            scores.append(player.get_total_match_history_score(self))
        return scores

    def is_building_already(self):
        """
        The provided function `is_building_already` checks if the `game_event`
        list of the object is non-empty and the object is not full.

        Returns:
            bool: The output returned by the `is_building_already` function is `True`.

        """
        return len(self.game_event) > 0 and not (self.full)

    def remove_player_from_match(self, player):
        """
        This function removes a player from a match by removing the player's game
        event registration and updating the match's full status.

        Args:
            player (): The `player` input parameter is passed as an argument to
                the `remove_game_event()` method of the player object.

        """
        player.remove_game_event(self)
        if player in self.game_event:
            self.game_event.remove(player)
        self.full = False

    def all_players_satisfy_min_games(self):
        """
        This function checks if all players have played more than their minimum
        game limit.

        Returns:
            bool: The output returned by this function is `True`.

        """
        return all(
            player.game_count > player.rules["minGamesTotal"]
            for player in self.game_event
        )

    def destruct(self):
        """
        This function "destruct" removes the event references for all the players
        that have the object as a game event and resets the "full" and "game_event"
        attributes of the object to empty lists.

        """
        for player in self.game_event:
            player.remove_game_event(self)
        self.game_event = []
        self.full = False

    def self_destruct_if_unneccessary(self):
        """
        This function destroys the object only if all players satisfy a minimum
        games condition.

        """
        if self.all_players_satisfy_min_games():
            self.destruct()

    def self_destruct_if_incomplete(self):
        """
        This function destroys the object if it is incomplete (i.e., not fully initialized).

        """
        if not (self.full):
            self.destruct()

    def get_players_available_to_swap(self, other_match):
        """
        This function gets the list of players who can be swapped from the current
        match to another match (hypothetically).

        Args:
            other_match (): The `other_match` parameter is a hypothetical match
                object used to check which players from the current match can be
                added to the other match without violating any constraints.

        Returns:
            list: The output of the function `get_players_available_to_swap()` is
            a list of players that are available to be swapped with players from
            another match.

        """
        available_players = []
        for player in self.game_event:
            if other_match.hypothetically_player_can_be_added(player):
                available_players.append(player)
        return available_players

    def logps(self, ps):
        """
        The given function `logps` prints the `player_name` of each element within
        the list `ps`.

        Args:
            ps (list): The `ps` input parameter is a list of PlayerStates (object/type
                not explicitly defined).

        """
        for p in ps:
            print(p.player_name)

    def get_inverse_players(self, players):
        """
        The function `get_inverse_players` takes a list of players and returns a
        list of players who are not present among the given list of players.

        Args:
            players (list): The `players` input parameter is a list of players who
                have already played their turns. The function iterates over the
                `game_event` list and for each event adds any player that is not
                already on the `players` list to the inverse list.

        Returns:
            list: The function takes a list of players (`players`) and returns a
            list of all players who are not included In the `self.game_event` list.

        """
        inverse = []
        for p in self.game_event:
            if not (p in players):
                inverse.append(p)
        return inverse

    def compare_histories_stay(self, group, stay, go):
        """
        This function takes three parameters: `group`, `stay`, and `go`, and it
        returns a list of dictionaries containing the score for each player based
        on their history of staying or going.

        Args:
            group (list): The `group` input parameter is a list of players and it
                is used to loop through each player's history scores.
            stay (): The `stay` input parameter passed to the `get_sum_history()`
                method of each player object within the `for p.. loop`.
            go (): The `go` input parameter is used to get the sum history of a
                player's moves for the "go" option.

        Returns:
            dict: The function "compare_histories_stay" returns a list of dictionaries
            containing scores for each player based on their history of staying
            or going.

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


    def get_sad_players_and_self(self):
        """
        This function takes a "self" parameter and returns a list of dictionaries
        representing sad players for the current timeslot.

        Returns:
            dict: The function returns a list of dictionaries called `sad_players`.

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
        This function calculates the difference ( delta ) between the history
        scores of two players ( self and other_player ), ignoring the score of a
        specified player ( ignore_player ).

        Args:
            other_player (): The `other_player` parameter is passed to the
                `check_history_score` method of the `other_player`, allowing it
                to evaluate and contribute to the calculation of the history delta.
            ignore_player (): The `ignore_player` input parameter is used to exclude
                the player being passed as `self` from the calculation of the
                history delta.

        Returns:
            int: The output returned by this function is `0`.

        """
        history_delta = 0
        for p in self.game_event:
            if p != ignore_player:
                history_delta += other_player.check_history_score(p)
        return history_delta
    
    def player_in_game(self, player):
        """
        This function checks whether the given `player` object is present inside
        the list of game events stored within the instance (i.e., whether it's
        currently participating or playing the game).

        Args:
            player (): The `player` input parameter is passed as an object of the
                `Player` class and it is used to search for the player with the
                same ID as the `player` object inside the list of game events.

        Returns:
            bool: Based on the code provided:
            
            The output returned by this function is `False`.

        """
        res = False
        for p in self.game_event:
            if p.id == player.id:
                res = True
        return res
    

    # FIGURE OUT HOW THIS IS DUPLICATING PLAYERS!
    def swap_with_best_candidate(self, out_player, swap_candidates):
        """
        This function swaps two players between two games if it's beneficial to
        the current game and both players are not already on the same team.

        Args:
            out_player (str): The `out_player` parameter is the player that should
                be swapped with a player from the other game.
            swap_candidates (dict): The `swap_candidates` parameter is a list of
                tuples containing two players: the player to swap with and the
                player's game object.

        """
        if swap_candidates:
            i = 0
            can_swap = False
            while i < len(swap_candidates):
                in_player = swap_candidates[i]['p']
                o_game = swap_candidates[i]['g']
                c1 = in_player in self.game_event
                c2 = in_player == out_player
                c3 = out_player in o_game.game_event
                if c1 or c2 or c3:
                    i += 1
                else:
                    can_swap = True
                    break
            if can_swap:
                self.remove_player_from_match(out_player)
                o_game.remove_player_from_match(in_player)
                self.force_player_to_match(in_player)
                o_game.force_player_to_match(out_player)
