from .utils import *
import copy


class Player:
    def __init__(self, player_obj, flight_id, availability_template, rules):
        """
        This function initializes an object of a class that represents a player's
        availability for a flight. It sets attributes such as the player's ID and
        name and the availability score calculated based on a template and the
        rules defined for the game.

        Args:
            player_obj (): The `player_obj` input parameter provides information
                about the player's availability and other relevant details that
                are used to calculate the availability score.
            flight_id (int): The `flight_id` input parameter specifies the specific
                flight for which the Availability object is being created.
            availability_template (dict): The `availability_template` input parameter
                is a dictionary that specifies the initial availability assumptions
                for each day of the flight.
            rules (dict): The `rules` input parameter provides a dictionary of
                custom rules that define how to handle specific scenarios during
                game planning.

        """
        self.rules = copy.deepcopy(rules)
        self.player_obj = player_obj
        self.id = player_obj.id
        self.player_name = player_obj.player_name
        availability = player_obj.get_availability_obj_for_flight(flight_id)
        self.availability_score, self.availability = update_availability_template(
            availability_template, availability, rules["assumeBusy"]
        )
        self.game_count = 0
        self.other_player_history = {}
        self.days = []
        self.weeks = []
        self.potentials = []
        self.satisfied = False
        self.captain_count = 0
        self.availability_score_greater_than_mean = False
        exceptions = []
        for key in self.rules['except']:
            if self.id in self.rules['except'][key]:
                exceptions.append(key)
        for key in exceptions:
            exception_fixers[key](self)
        del self.rules['except']

    def __hash__(self):
        """
        This is a Python function definition for the `__hash__` method of an object.
        It returns the `id` attribute of the object.

        Returns:
            int: The output returned by this function is `None`.

        """
        return self.id

    def set_availability_score_relation(self, mean_score):
        """
        This function sets the "availability score greater than mean" relation for
        the object by comparing the object's availability score to a given mean score.

        Args:
            mean_score (float): The `mean_score` input parameter sets the reference
                point for the comparison of availability scores.

        """
        self.availability_score_greater_than_mean = self.availability_score > mean_score

    def __eq__(self, other):
        """
        This function defines an `__eq__()` method for a `Player` object that
        checks if two players have the same ID.

        Args:
            other (): The `other` input parameter is used to compare the current
                object with another object of the same type (in this case `Player`).

        Returns:
            bool: The output returned by this function is "False".

        """
        if isinstance(other, Player):
            return self.id == other.id
        return False
    
    def find_potential_slots_in_current_layout(self, gameslots):
        """
        This function finds potential slots for new games based on the availability
        of existing games and constraints defined by the "rules" dictionary.

        Args:
            gameslots (dict): The `gameslots` input parameter is a list of Gameslot
                objects that represents the available game slots for scheduling.

        Returns:
            list: The output returned by this function is a list of games (i.e.,
            'g') that have availability and fit the rules defined by 'self.days'
            and 'self.rules'.

        """
        potentials = []
        for g in gameslots:
            if self.availability[g.timeslot_id] == AVAILABLE or self.availability[g.timeslot_id] == AVAILABLE_LP:
                if self.days.count(g.day_number) < self.rules["maxGamesDay"] and self.days.count(g.day_number) < self.rules["maxGamesDay"]:
                    potentials.append(g)
        self.potentials = potentials
        return potentials

    def add_game_event(self, gameslot):
        """
        This function adds a new game event to the object's history and updates
        various statistics based on the event. It checks if the minimum or maximum
        number of games has been reached and updates the satisfied flag accordingly.

        Args:
            gameslot (dict): The `gameslot` input parameter is a dictionary that
                contains information about a specific game session (e.g., game
                title played and date/time of play), and it is used to update the
                game counting information and history logging for the agent.

        """
        game_event = gameslot.game_event
        self.game_count += 1
        self.satisfied = (self.game_count >= self.rules["minGamesTotal"]) and (
            self.game_count <= self.rules["maxGamesTotal"]
        )
        for player in game_event:
            if player != self:
                self.add_history(player)
        self.days.append(gameslot.day_number)
        self.weeks.append(gameslot.week_number)

    def remove_game_event(self, gameslot):
        """
        This function removes a game event from a `GameSession` object by updating
        the `game_count`, `satisfied`, and `history` attributes and removing the
        game event from the `days` and `weeks` lists.

        Args:
            gameslot (): The `gameslot` parameter is an object representing a
                specific slot (i.e., day and time) at which a game can be played.

        """
        game_event = gameslot.game_event
        self.game_count -= 1
        self.satisfied = (self.game_count >= self.rules["minGamesTotal"]) and (
            self.game_count <= self.rules["maxGamesTotal"]
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
        This function checks if a player's ID is present In the "other_player_history"
        attribute of the class and returns their score if it is or returns 0 if not.

        Args:
            player (): The `player` input parameter is passed as an object to the
                `check_history_score()` function and it represents the player whose
                history score is being checked.

        Returns:
            int: The output returned by this function is 0.

        """
        if player.id in self.other_player_history:
            return self.other_player_history[player.id]
        else:
            return 0

    def get_most_history_player_in_match(self, match):
        """
        This function returns the player with the most history (i.e., the player
        who has been involved with the current player the most) among all players
        other than the current player and the starting player.

        Args:
            match (dict): The `match` input parameter is a `Match` object containing
                information about the current game match being analyzed. It contains
                an event list representing the order of events (such as player
                actions or game state changes) that occurred during the match.

        Returns:
            : The function `get_most_history_player_in_match` takes a `match`
            object as input and returns the player with the most history (i.e.,
            the player who has played the most number of games) among all players
            involved In the match.
            
            The output of this function is a `player` object representing the
            player with the most history In the match.

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
        This function retrieves the most common player and their count from a
        dictionary of player history data.

        Returns:
            dict: The function returns a dictionary with the most common player
            and its count as follows:
            
            {0: 0}

        """
        if len(self.other_player_history):
            max_key = max(self.other_player_history, key=self.other_player_history.get)
            return {max_key: self.other_player_history[max_key]}
        else:
            return {0: 0}

    def get_total_match_history_score(self, match):
        """
        This function calculates the total match history score for a given match
        by adding up the history scores of all players involved In the game.

        Args:
            match (): The `match` input parameter is a game event that contains a
                list of player objects representing the players participatingin
                the game.

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
        This function adds 1 to the number of times a player has interacted with
        another player.

        Args:
            player (): The `player` input parameter is passed as an object that
                contains the player's information.

        """
        if player.id in self.other_player_history:
            self.other_player_history[player.id] += 1
            player.other_player_history[self.id] += 1
        else:
            self.other_player_history[player.id] = 1
            player.other_player_history[self.id] = 1

    def subtract_history(self, player):
        """
        This function subtracts one from the `other_player_history` dictionary of
        both objects for the given player.

        Args:
            player (): The `player` input parameter is used to specify the player
                whose history is being subtracted from the current player's history.

        """
        self.other_player_history[player.id] -= 1
        player.other_player_history[self.id] -= 1

    def get_history(self, player):
        """
        The `get_history()` function retrieves the history of moves made by a
        specified player (represented by `player`) from a cache (`self.other_player_history`)
        and returns it if it exists; otherwise returns 0.

        Args:
            player (): The `player` input parameter is used to determine which
                player's history should be retrieved.

        Returns:
            list: The output returned by this function is 0.

        """
        if player.id in self.other_player_history:
            return self.other_player_history[player.id]
        else:
            return 0

    def get_sum_history(self, players):
        """
        This function calculates the average history of a set of players by getting
        the history of each player and dividing the sum of those histories by the
        number of players.

        Args:
            players (list): The `players` input parameter is a list of players'
                histories that are being summed together to calculate the total
                history sum.

        Returns:
            float: The output returned by the function is `res / count`, which is
            the average of the values returned by `self.get_history()` for each player.

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
        This function prints information about a player's satisfaction and game
        count and identifies the most common player using an available availability
        score.

        Args:
            dofilter (None): The `dofilter` input parameter is not used or defined
                within the provided code snippet.

        """
        print(
            self.player_name,
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
        This function checks if a game is available for play by checking the
        availability of the specific time slot requested (gameslot).

        Args:
            gameslot (): The `gameslot` input parameter is a tuple containing the
                timeslot ID for which availability should be checked.

        Returns:
            bool: The function `check_game_availability` returns a boolean value
            indicating whether a game is available or not.

        """
        res = self.availability[gameslot.timeslot_id]
        return res == AVAILABLE or res == AVAILABLE_LP