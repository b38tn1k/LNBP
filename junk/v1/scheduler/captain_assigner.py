from .player import *
from .gameslots import *
from .utils import *
from random import shuffle

class CaptainAssigner():
    def __init__(self, flight):
        """
        This function initalizes an object of the class "Flight" with the given
        flight and initializes the members self.flight_obj and self.flight_id. It
        then initializes a list of gameslots based on a set of rules and the
        template of the game. The gameslots are also populated with temporary
        players from the list of flight players.

        Args:
            flight (): The `flight` input parameter is an instance of the `Flight`
                class that contains information about a specific flight (e.g., its
                ID and list of players).

        """
        self.flight_obj = flight
        self.flight_id = flight.id
        self.rules = tempRules
        template, self.gameslots = findAllGameSlots(flight, self.rules)
        self.players = []
        for player in flight.players:
            self.players.append(Player(player, self.flight_id, template, self.rules))
        for g in self.gameslots:
            if len(g.temp_players) != 0:
                # print(g.temp_players)
                
                for p in self.players:
                    if p.id in g.temp_players:
                        g.force_player_to_match(p)
                # print([p.id for p in g.game_event])
                # print()
        



    def run(self):
        """
        This function `run` takes no arguments and has three main responsibilities:
        1/ Resetting captains and recalculating players.
        2/ Assigning captains to games based on certain conditions.
        3/ Returning a Boolean value indicating whether all players have been
        captained at least once and all games have had captains assigned.

        Returns:
            bool: Based on the code provided:
            
            The output returned by this function is a boolean value indicating
            whether all players have been captained at least once and all games
            have been captained.

        """
        for i in range(POOL_ITERATIONS):
            self.reset_captaining()
            self.recalculate_players()
            self.assign_captains()
            self.recalculate_players()
            cm, gc = self.all_players_captained_minimum(), self.all_games_captained()
            if cm and gc:
                break
        
        assignment_list = []
        for game in self.gameslots:
            if game.captain and game.event_obj:
                assignment_list.append([game.start_time, game.captain.player_name])
                # print(game.start_time, game.captain.player_name)
                game.event_obj.update_captain_by_id(game.captain.id)
                # print(game.event)
        sorted_data = sorted(assignment_list, key=lambda x: x[0])
        # for s in sorted_data:
        #     print(s[0].strftime("%m %d, %H:%M"), s[1])
        return self.all_players_captained_minimum() and self.all_games_captained()

        

    @log_timer
    def recalculate_players(self):
        """
        This function updates the `satisfied` attribute of each player by checking
        if they have played enough games (based on their individual rules) and
        incrementing the corresponding counter if they have.

        """
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
                p.satisfied = satisfied[p.id] >= p.rules["minGamesTotal"]



    def all_players_captained_minimum(self):
        """
        The function `all_players_captained_minimum` checks whether all players
        have been captained at least as many times as their minimum captaincy rule.

        Returns:
            bool: The output returned by this function is "True".

        """
        count = 0
        for p in self.players:
            count += (p.captain_count >= p.rules["minCaptained"])
        return count == len(self.players)
    
    def all_games_captained(self):
        """
        This function checks if all games slots are occupied by players with a
        captain flag set to None. If any game slot has a player with a captain
        flag set to True or blank (None), the function returns False.

        Returns:
            bool: The output returned by this function is `True`.

        """
        for g in self.gameslots:
            if g.full is True and g.captain is None:
                return False
        return True
    
    def reset_captaining(self):
        """
        This function resets the captain information for all players and gameslots.

        """
        for p in self.players:
            p.captain_count = 0
        for g in self.gameslots:
            g.captain = None
    
    def assign_captains(self):
        """
        This function assigns captains to gameslots where there are more players
        than available slots and ensures that no player is assigned to too many
        games or too few games based on their rules.

        """
        assigned = set()
        self.recalculate_players()
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
        uncaptained_games = [g for g in self.gameslots if g.captain is None]
        over_captained = [p for p in self.players if p.captain_count > p.rules['maxCaptained']]
        under_captained = [p for p in self.players if p.captain_count < p.rules['minCaptained']]
