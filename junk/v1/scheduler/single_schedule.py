from app.models.player import Player 
import statistics
from random import shuffle, choice, seed, random
from itertools import combinations
from .utils import *
from .gameslots import *
from .player import *

@log_timer
def init_histories(players):
    """
    The `init_histories` function initializes the `other_player_history` dictionary
    for each player with the ID of every other player as a key and a value of 0.

    Args:
        players (list): The `players` input parameter is a list of Player objects
            that the function iterates over to initialize each Player's
            other_player_history dictionary with zero values for all other players.

    """
    for player in players:
        for p in players:
                player.other_player_history[p.id] = 0
@log_timer
def get_histories(potential_game):
    """
    The `get_histories` function calculates the total sum of the other players'
    history for a given player's history.

    Args:
        potential_game (list): The `potential_game` input parameter is a dictionary
            of players and their respective other players' history values.

    Returns:
        int: The output returned by this function is 0.

    """
    sum_history = 0
    for player in potential_game:
        for p in potential_game:
                sum_history += player.other_player_history[p.id]
    return sum_history

@log_timer
def check_potential_game_length(potential_game, rules):
    """
    This function checks whether a potential game meets the rules specified by
    checking the length of the game and comparing it to the length of the rules.

    Args:
        potential_game (list): The `potential_game` input parameter is a list of
            game tiles that represents the current state of the game.
        rules (int): The `rules` input parameter is a boolean indicator that
            specifies the minimum length of a valid game.

    Returns:
        bool: The function `check_potential_game_length` takes two arguments:
        `potential_game`, which is a list of cards representing the current state
        of the game board (i.e. the positions where cards have been played), and
        `rules`, which is a dictionary defining the game rules.
        
        The function simply checks if the length of the `potential_game` list does
        not match the value specified by the key "length" of the `rules` dictionary.
        
        So the output of the function would be `True` for any game state where the
        number of cards played differs from the specified length.

    """
    return (len(potential_game) != rules)

@log_timer
def contains_high_game_count_player(potential_game, average_game_count):
    """
    The function `contains_high_game_count_player` takes two arguments: `potential_game`
    and `average_game_count`.

    Args:
        potential_game (dict): The `potential_game` parameter is the game being
            analyzed for high game count players.
        average_game_count (int): The `average_game_count` parameter is used as a
            threshold to check if a player's game count is significantly higher
            than the average game count.

    Returns:
        bool: The output returned by this function is `False`.

    """
    return any(player.game_count > average_game_count for player in potential_game)

@log_timer
def contains_players_already_scheduled(players_scheduled, potential_game):
    """
    This function takes two arguments: `players_scheduled` and `potential_game`,
    and it returns `True` if there are any players already scheduled to play that
    are also present within the `potential_game`.

    Args:
        players_scheduled (list): The `players_scheduled` input parameter is a
            list of players that have already been scheduled for games.
        potential_game (list): The `potential_game` input parameter is a list of
            players that may be scheduled for a game.

    Returns:
        bool: The output returned by the function `contains_players_already_scheduled`
        is `True` if any of the players In `potential_game` are already scheduled
        and `False` otherwise.

    """
    return any(player in players_scheduled for player in potential_game)

@log_timer
def player_fails_day_week_count(potential_game, day, week):
    """
    This function checks whether a player has reached the maximum number of games
    allowed for a specific day or week within a list of potential games.

    Args:
        potential_game (list): The `potential_game` input parameter is a list of
            games that are being checked to see if they fit the rules defined by
            the `player.rules` dictionary.
        day (int): The `day` input parameter is a fixed date that the function
            checks to see if the player has already played a game on that day.
        week (int): The `week` input parameter specifies the number of weeks that
            a player can play games during a single day.

    Returns:
        bool: The output returned by this function is `False`. The function checks
        each player's `days` and `weeks` attributes and compares the number of
        games played on a given day or week with the maximum allowed value specified
        In the player's `rules` dictionary. If any player has played more than the
        maximum allowed games on a day or week the function returns `True`.

    """
    for player in potential_game:
        day_count = player.days.count(day)
        week_count = player.weeks.count(week)
        if day_count >= player.rules['maxGamesDay'] or week_count >= player.rules['maxGamesWeek']:
            return True
    return False

@log_timer
def all_players_satisfied(potential_game):
    """
    This function checks whether all players have their desired number of games
    satisfied or not.

    Args:
        potential_game (list): The `potential_game` input parameter is a list of
            players and their associated game counts before any games are removed
            to satisfy the minimum/maximum game constraints.

    Returns:
        bool: The output returned by this function is `all_satisfied`.

    """
    all_satisfied = True
    over_scheduled = False
    for player in potential_game:
        if player.game_count < player.rules["minGamesTotal"]:
            all_satisfied = False
        if player.game_count >= player.rules["maxGamesTotal"]:
            over_scheduled = True
    return all_satisfied or over_scheduled

@log_timer
def get_play_count(potential_game):
    """
    The given function `get_play_count` takes a list of players as input and returns
    the total number of games played by all the players.

    Args:
        potential_game (list): The `potential_game` parameter is an iterable object
            (such as a list or tuple) of players. The function loops through each
            player and calculates the game count for that player by summing up the
            game counts of all the other players.

    Returns:
        int: The output returned by the `get_play_count` function is `sum_history`,
        which is equal to the sum of the `game_count` attributes of all players
        of all games played by them. Since there is no specific game or player
        input passed to the function and none are mentioned explicitly inside it
        either so undefined cannot return anything . There wont be any output
        because sum history will always be zero as none of the player or games
        have any count.

    """
    sum_history = 0
    for player in potential_game:
        for p in potential_game:
                sum_history += player.game_count
    return sum_history

def create_failure_scenarios():
    """
    This function creates a dictionary of failure scenarios for a game schedule
    optimization problem.

    Returns:
        dict: The output returned by the function `create_failure_scenarios` is
        an empty dictionary `{}`.

    """
    failing_scenarios = {}
    failing_scenarios['available slots'] = 0
    failing_scenarios['game length'] = 0
    failing_scenarios['players already scheduled'] = 0
    failing_scenarios['day or week failure'] = 0
    failing_scenarios['all players satisfied'] = 0
    return failing_scenarios

class SingleSchedule:
    @log_timer
    def __init__(self, flight, template, gameslots):
        """
        This function initiates an instance of a class called `Flight` by passing
        it a `flight`, `template`, and `gameslots` objects.

        Args:
            flight (): The `flight` input parameter passed to the `__init__()`
                method is used to define the `Flight` object that contains information
                about the flight for which the Gameslot object is being created.
            template (dict): The `template` input parameter is used to pass a
                pre-defined set of rules for the flight to the constructor of the
                class.
            gameslots (list): The `gameslots` input parameter is a list of Gameslot
                objects that defines the available courts for the players to choose
                from.

        """
        self.flight_obj = flight
        self.flight_id = flight.id
        self.rules = tempRules
        self.gameslots = gameslots
        self.gameslot_dict = {}
        shuffle(self.gameslots)
        self.gameslots = sorted(
            self.gameslots, key=lambda gs: gs.court_name, reverse=True
        )
        self.players = []
        for player in flight.players:
            self.players.append(Player(player, self.flight_id, template, self.rules))
        self.players = sorted(
            self.players, key=lambda player: player.availability_score
        )

    def check_escape_conditions(self, log=False):
        """
        This function checks if a set of players satisfy certain escape conditions
        based on their game count and schedule. It returns True if all players
        meet the conditions and False otherwise.

        Args:
            log (bool): The `log` input parameter is an optional boolean value
                that controls whether logs are printed to the console when certain
                conditions are met.

        Returns:
            bool: The output returned by this function is "True" if all the escape
            conditions are satisfied (i.e., all players have enough days and weeks
            to play), and "False" otherwise.

        """
        for player in self.players:
            # players have min games
            if player.satisfied == False:
                if log:
                    print("player satisfied")
                return False
            # players aren't over scheduled
            if player.game_count > player.rules['maxGamesTotal']:
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
                if (
                    days[key] > player.rules["maxGamesDay"]
                ):
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
                if (
                    weeks[key] > player.rules["maxGamesWeek"]
                ):
                    if log:
                        print("max weeks")
                    return False
        return True

    def check_all_conditions(self):
        """
        This function checks if a given list of players satisfies all the conditions
        defined by the game rules. It returns True if all conditions are satisfied
        and False otherwise.

        Returns:
            bool: The output returned by this function is `True` if all conditions
            are satisfied and `False` otherwise.

        """
        for player in self.players:
            if player.satisfied == False:
                return False
            if player.game_count > player.rules['maxGamesTotal']:
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
                if (
                    days[key] > player.rules["maxGamesDay"]
                ):
                    return False
                
            weeks = {}
            for w in player.weeks:
                if w in weeks:
                    weeks[w] += 1
                else:
                    weeks[w] = 1
            for key in weeks:
                if (
                    weeks[key] > player.rules["maxGamesWeek"]
                ):
                    return False   
        return True
    
    def generate_timeslot_player_pool(self):
        """
        This function generates a timeslot player pool for a set of gameslots by
        collecting available players and filtering them based on the specified rules.

        Returns:
            dict: The output of the `generate_timeslot_player_pool` function is a
            dictionary `tpp` with the following structure:
            
            	- `tpp` is a dictionary with timeslots as keys and containing the
            following values:
            	+ `all`: list of all players available for that timeslot.
            	+ `filtered`: list of available players (i.e., those who have
            availability == AVAILABLE or UNK and the rules["assumeBusy"] is False)
            for that timeslot.
            	+ `times`: list of games that are scheduled during that timeslot.
            	+ `day`: day number of the timeslot.
            	+ `week`: week number of the timeslot.
            	+ `available_slots`: minimum number of concurrent games allowed for
            that timeslot.
            	+ `sgames`: list of schedule games (i.e., games that are already
            scheduled) for that timeslot.
            	+ `pgames`: list of potential games (i.e., games that could be
            scheduled) for that timeslot.

        """
        ts = set([g.timeslot_id for g in self.gameslots])
        tpp = {} # timeslot player pool
        for t in ts:
            tpp[t] = {}
            tpp[t]['all'] = [p for p in self.players if p.availability[t] != UNAVAILABLE]
            tpp[t]['filtered'] = [p for p in tpp[t]['all'] if p.availability[t] == AVAILABLE or (p.availability[t] == UNK and self.rules["assumeBusy"] is False)]
            tpp[t]['times'] = [g for g in self.gameslots if g.timeslot_id == t]
            tpp[t]['day'] = tpp[t]['times'][0].day_number
            tpp[t]['week'] = tpp[t]['times'][0].week_number
            tpp[t]['available_slots'] = min(len(tpp[t]['times']), self.rules["maxConcurrentGames"])
            tpp[t]['sgames'] = []
            tpp[t]['pgames'] = [] # all potential games
            game_grabber = tpp[t]['filtered'] if len(tpp[t]['filtered']) > self.rules["playersPerMatch"] else tpp[t]['all']
            if len(game_grabber) >= self.rules["playersPerMatch"]:
                for g in combinations(tpp[t]['all'], self.rules["playersPerMatch"]):
                    tpp[t]['pgames'].append(g)
        return tpp, ts

    @log_timer
    def runCA(self):
        """
        This function calculates potential games for each player (or group of
        players) based on their preferred courts and schedules; It also matches
        players with suitable games to create a schedule. The following steps
        summarize its operation:
        	- Initialize a dictionary containing court data for timeslots.
        	- Loop through timeslots:
        	- Create lists of scheduled games for each timeslot
        	- Add new games that are not blocked by existing ones or preferences.
        	- When there is a match (e.g., when two players prefer the same court but
        at different times), mark the game as added and continue looping to ensure
        all matches find potential games. If no match can be made during the current
        iteration of timeslots. It updates all relevant player schedules based on
        added matches.
        	- Repeat until all possible games for a particular timeslot have been
        processed and all players have at least one game; break out of loops when
        there are no more matching players or games. Finally—calculate new preferred
        courts based on player history data to recreate a full schedule for your
        tennis league.

        """
        tpp, ts = self.generate_timeslot_player_pool()
        ts_list = list(ts)
        shuffle(ts_list)
        all_scheduled_games = []
        init_histories(self.players)
        total_players = len(self.players)
        total_games_added = 0
        loop_count = 0
        games_considered = 0
        while True:
            game_added = 0
            timeslot_count = 0
            # print("LOOP", loop_count)
            loop_count += 1
            # failing_scenarios = create_failure_scenarios()
            already_added = False
            for t in ts_list:
                # d = tpp[t]['times'][0]
                # print(d.start_time)
                # print("TIMESLOT", timeslot_count)
                timeslot_count += 1
                # Track which players have already been scheduled
                players_scheduled = set([p for p in [g for g in tpp[t]['sgames']]])
                
                # Game selection priority sorting
                sorted_games = sorted(tpp[t]['pgames'], key=lambda x: get_histories(x))                    
                already_added = False

                average_game_count = self.get_average_game_count()
                # print('average game count', average_game_count)
                lower_than_average = []
                for g in sorted_games:
                    add_game = False
                    for p in g:
                        if p.game_count < average_game_count:
                            add_game = True
                    if add_game:
                        lower_than_average.append(g)

                # print("length", len(lower_than_average), len(sorted_games))

                if len(lower_than_average) != 0:
                    sorted_games = lower_than_average

                day, week = tpp[t]['day'], tpp[t]['week']

                for potential_game in sorted_games:
                    games_considered += 1

                    # only consider 1 game per loop
                    if already_added:
                        break

                    # Apply Rule 1: Ensure we have available slots for this timeslot
                    if tpp[t]['available_slots'] == 0:
                        # failing_scenarios['available slots'] += 1
                        break

                    if check_potential_game_length(potential_game, self.rules['playersPerMatch']):
                        # failing_scenarios['game length'] += 1
                        continue

                    # Apply Rule 2: Check if any player in this game is already scheduled for this timeslot
                    if contains_players_already_scheduled(players_scheduled, potential_game):
                        # failing_scenarios['players already scheduled'] += 1
                        continue

                    # Apply Rule 3: Count how many times the player has already played that day, week
                    if player_fails_day_week_count(potential_game, day, week):
                        # failing_scenarios['day or week failure'] += 1
                        continue

                    # Apply Rule 4: Don't schedule games where all players have a game_count > tempRules["minGamesTotal"] 
                    # Apply Rule 5: Don't schedule games where any player has a game_count >= tempRules["maxGamesTotal"]
                    if all_players_satisfied(potential_game):
                        # failing_scenarios['all players satisfied'] += 1
                        continue
                    
                    # All constraints satisfied, so we schedule this game
                    tpp[t]['sgames'].append(potential_game)
                    tpp[t]['available_slots'] -= 1
                    game_added += 1
                    total_games_added += 1
                    already_added = True
                    # print("GAMES CONSIDERED", games_considered)
                    # print()
                    # for key in failing_scenarios:
                    #     if failing_scenarios[key] != 0:
                    #         print(key, failing_scenarios[key])
                    # print()

                    # Track all scheduled games also
                    all_scheduled_games.append(potential_game)
                    
                    # Update tracking variables
                    # players_scheduled.update(potential_game)
                    # print(len(players_scheduled))

                    for player in potential_game:
                        player.days.append(tpp[t]['day'])
                        player.weeks.append(tpp[t]['week'])
                        player.game_count += 1

                    for player in potential_game:
                        for p in potential_game:
                            if p is not player:
                                    player.other_player_history[p.id] += 1
                    # At this point, tpp[t]['sgames'] contains some scheduled games for timeslot t
                    # print([[p.id for p in g] for g in tpp[t]['sgames']])
                    # only consider 1 game per loop
                    if already_added:
                        # print("CONTINUE", total_games_added)
                        continue
            # print()
            # for key in failing_scenarios:
            #     print(key, failing_scenarios[key])
            # print()
            if game_added == 0:
                # print()
                # print("TOTAL GAMES ADDED: ", total_games_added, len(all_scheduled_games))
                break
        self.recalculate_players()

        counter = 0
        for t in ts_list:
            tpp[t]['times'] = sorted(tpp[t]['times'], key=lambda x: x.court_name)
            if len(tpp[t]['sgames']) != 0:
                for i, sg in enumerate(tpp[t]['sgames']):
                    gs = tpp[t]['times'][i]
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
            common_elments.intersection_update(unsatisfied[counter+1].potentials)
            if len(common_elments) != 0:
                # unsatisfied_friends.append({"f1": unsatisfied[counter], "f2": unsatisfied[counter + 1], "overlap": common_elments})
                unsatisfied_friends.append({"players": [unsatisfied[counter], unsatisfied[counter + 1]] , "overlap": common_elments})
            counter += 1
        if len(unsatisfied_friends) != 0:
            f2_old = unsatisfied_friends[0]["players"][1]
            f_old = unsatisfied_friends[0]
            for f in unsatisfied_friends:
                # print(f["players"][0].player_name, f["players"][1].player_name)
                if f2_old == f["players"][0]:
                    common_elments = set(f["overlap"])
                    common_elments.intersection_update(f_old["overlap"])
                    if len(common_elments) != 0:
                        new_group = {"players": [f_old["players"][0], f_old["players"][1], f["players"][1]], "overlap": common_elments}
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
                        # print([p.player_name for p in f_old["players"]])
                        # print([p.player_name for p in gr["players"]])
                        p1 = [p for p in f_old["players"]]
                        p2 = [p for p in gr["players"]]
                        for np in p2:
                            if not np in p1:
                                p1.append(np)
                        # print([p.player_name for p in p1])

                        new_group = {"players": p1, "overlap": common_elments}
                        third_iteration.append(new_group)
                        # print("ANOTHER MATCH", len(common_elments))
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


                


        # print(len([g for g in self.gameslots if g.full is True]))

    def summarise_tests(self):
        """
        This function `summarize_tests` takes no arguments and returns a dictionary
        with four key-value pairs:
        	- `all_players_satisfied`: The value of the method `all_players_satisfied()`
        	- `player_days_satisfied`: The value of the method `player_days_satisfied()`
        	- `player_weeks_satisfied`: The value of the method `player_weeks_satisfied()`
        	- `no_players_overscheduled`: The value of the method `no_players_overscheduled()`

        Returns:
            dict: The output returned by the function `summarise_tests` is a
            dictionary with four keys:
            
            	- `all_players_satisfied`: a boolean value indicating if all players
            are satisfied
            	- `player_days_satisfied`: a list of booleans indicating if each
            player's days are satisfied
            	- `player_weeks_satisfied`: a list of booleans indicating if each
            player's weeks are satisfied
            	- `no_players_overscheduled`: a boolean value indicating if no players
            are overscheduled.

        """
        result = {}
        result['all_players_satisfied'] = self.all_players_satisfied()
        result['player_days_satisfied'] = self.player_days_satisfied()
        result['player_weeks_satisfied'] = self.player_weeks_satisfied()
        result['no_players_overscheduled'] = self.no_players_overscheduled()
        return result

    def backup_gameslots(self):
        """
        This function creates a copy of all the gameslots associated with the
        current instance (self) and returns a list of those copies.

        Returns:
            list: The output returned by the `backup_gameslots` function is a list
            of copies of the gameslots.

        """
        b = []
        for g in self.gameslots:
            b.append(g.copy_with_events())
        return b

    def quick_log_game_count(self):
        """
        This function quick_log_game_count takes an object of type player list and
        returns a string representation of the game count for each player separated
        by a space.

        Returns:
            str: The output returned by the function `quick_log_game_count` is the
            string `" 123 "`.

        """
        myString = ""
        for p in self.players:
            myString += str(p.game_count) + " "
        # print(myString)
        return myString.strip()

    def clear_everything(self):
        """
        This function clears all game events and sets the full status to false for
        all game slots (g) and also recreates the player calculations.

        """
        for g in self.gameslots:
            g.game_event = []
            g.full = False
        self.recalculate_players()

    def print_problems(self, res):
        """
        This function prints out the problems found by the game for each player
        during a round of the game.

        Args:
            res (dict): The `res` input parameter is a list of dictionaries
                representing the results of each player's turn.

        """
        i = 0
        for r in res:
            print("PROBLEM: ", i)
            i += 1
            r["game"].log()
            for p in r["players"]:
                print(p.player_name)
            print()

    @log_timer
    def recalculate_players(self):
        """
        This function recalculates the satisfaction of each player based on their
        game event participation and updates their other player history information.

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

    def get_days(self):
        """
        This function returns a dictionary of days where each day is a list of
        full slots (i.e., slots that have been fully booked).

        Returns:
            dict: The output of this function is a dictionary containing lists of
            `gameslot` objects for each day number.

        """
        full_slots = [slot for slot in self.gameslots if slot.full == True]
        days = {}
        for slot in full_slots:
            if slot.day_number in days:
                days[slot.day_number].append(slot)
            else:
                days[slot.day_number] = [slot]
        return days

    @log_timer
    def sort_out_preferences(self):
        """
        This function sorts out the preferences of players for each day and checks
        if a player is available for a particular game slot and decides how to
        swap the player between games if necessary.

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

    @log_timer
    def create_events(self, skip=False):
        """
        This function creates events for each game slot and timeslot combination
        within a flight schedule.

        Args:
            skip (bool): The `skip` input parameter of the `create_events` function
                is a boolean parameter that allows you to skip creating events for
                certain gameslots if they are already full or if the user has
                chosen to skip certain gameslots.

        """
        for gameslot in self.gameslots:
            if gameslot.full is True or skip is True:
                timeslot = gameslot.timeslot_obj
                court = gameslot.court_obj
                captain = None
                players = []
                for player in gameslot.game_event:
                    players.append(self.flight_obj.get_players_by_id(player.id))
                timeslot.create_event(court, players, captain)

    def all_players_satisfied(self):
        """
        This function checks if all players attached to the object (i.e. instances
        of Player) have their satisfaction value set to true (i.e. satisfied). If
        any player's satisfaction value is false (i.e. not satisfied), the function
        returns false. If all players are satisfied (i.e.

        Returns:
            bool: The output returned by this function is "True".

        """
        for player in self.players:
            if player.satisfied == False:
                return False
        return True
    
    def no_players_overscheduled(self):
        """
        This function checks whether any of the players have been overscheduled
        by checking each player's game count against their maximum number of games
        allowed. If any player has exceeded their limit; the function returns false.

        Returns:
            bool: The output returned by the function is `True`.

        """
        for player in self.players:
            if player.game_count > player.rules['maxGamesTotal']:
                return False
        return True

    def player_days_satisfied(self):
        """
        This function checks if a player has satisfied their daily play requirements
        by iterating over their schedule of games and calculating the number of
        games played on each day.

        Returns:
            bool: Based on the code provided:
            
            The output returned by this function is "True" if all players have
            played within their max number of games per day; otherwise (i.e., if
            at least one player has exceeded their limit), it returns "False".

        """
        for player in self.players:
            days = {}
            for day in player.days:
                if day in days:
                    days[day] += 1
                else:
                    days[day] = 1
            for key in days:
                if (
                    days[key] > player.rules["maxGamesDay"]
                ):
                    return False
        return True
    
    def player_weeks_satisfied(self):
        """
        This function checks whether a given set of players has satisfied the
        maximum games per week limit set by their rules for all weeks. If any
        player has exceeded the limit for any week (based on the number of games
        played that week), the function returns False.

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
                if (
                    weeks[key] > player.rules["maxGamesWeek"]
                ):
                    return False
        return True
    
    def get_player_days_unsatisfied(self):
        """
        This function 'get_player_days_unsatisfied' returns a list of players who
        have not played the maximum number of games allowed on a day as specified
        by their rules.

        Returns:
            dict: The function `get_player_days_unsatisfied` returns two things:
            
            1/ A list of players (`us`) who have more games on a day than their
            maximum allowed games for that day.
            2/ A dictionary (`bg`) where the keys are the player IDs and the values
            are the lists of game IDs for each player on that day.

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
                if (
                    days[key] > player.rules["maxGamesDay"]
                ):
                    us.append(player)
                    bg[player.id] = self.find_games_on_day_with_player(player, key)
        return us, bg
    
    
    def find_games_on_day_with_player(self, player, day):
        """
        This function finds all games on a given day ( día ) that include a specific
        player ( jugador ).

        Args:
            player (): The `player` input parameter is used to filter the list of
                games returned by the function.
            day (int): The `day` input parameter specifies the day for which games
                are to be found.

        Returns:
            list: The output returned by the function `find_games_on_day_with_player`
            is a list of `Game` objects that have the specified `player` and are
            scheduled on the specified `day`.

        """
        res = []
        for g in [g for g in self.gameslots if g.day_number == day]:
            if player in g.game_event:
                res.append(g)
        return res
    
    def log_player_days_unsatisfied(self):
        """
        This function prints the player names and their corresponding start times
        for each day that the player was unsatisfied.

        """
        p, d = self.get_player_days_unsatisfied()
        for i in p:
            print(i.player_name)
            for k in d[i.id]:
                print(k.start_time)
            print()

    def get_gameslots_by_day(self, day_number):
        """
        The function `get_gameslots_by_day` takes a `day_number` and returns a
        list of `gameslots` from a collection where the `day_number` attribute
        matches the input.

        Args:
            day_number (int): The `day_number` input parameter specifies which
                day's worth of gameslots the function should return.

        Returns:
            list: The function returns a list of gameslots where the "day_number"
            matches the day_number passed as an argument.

        """
        return [
            gameslot for gameslot in self.gameslots if gameslot.day_number == day_number
        ]

    def get_gameslots_by_week(self, week_number):
        """
        This function takes a `week_number` input and returns a list of `Gameslot`
        objects that have a `week_number` equal to the input.

        Args:
            week_number (int): The `week_number` input parameter specifies which
                week of gameslots to retrieve.

        Returns:
            list: The function "get_gameslots_by_week" returns a list of gameslots
            where the "week_number" matches the given week number.

        """
        return [
            gameslot
            for gameslot in self.gameslots
            if gameslot.week_number == week_number
        ]

    def log(self, dofilter=False):
        """
        This function calls the `log` method on all the players and gameslots
        objects stored within the `self` object.

        Args:
            dofilter (bool): The `dofilter` parameter is an optional argument that
                defaults to `False`. It is passed through to each item of the two
                lists (players and gameslots) as their log method's second argument.

        """
        for p in self.players:
            p.log(dofilter)
        for gs in self.gameslots:
            gs.log(dofilter)

    def get_average_game_count(self):
        """
        This function calculates the average game count for all players within a
        collection of objects (players).

        Returns:
            float: The output returned by this function is 3.

        """
        return sum([p.game_count for p in self.players]) / len(self.players)
    
    def get_average_failure_count(self):
        """
        This function calculates the average number of games a player has failed
        to meet the minimum game count requirement.

        Returns:
            float: The output returned by this function would be: `undefined`. The
            `sum` function cannot sum up the values of a list of abs(p.rules['minGamesTotal']
            - p.game_count) as there is no 'minGamesTotal' attribute or variable
            present.

        """
        return sum([abs(p.rules['minGamesTotal'] - p.game_count) for p in self.players]) / len(self.players)
    
    def average_player_satisfaction(self):
        """
        This function calculates the average player satisfaction by dividing the
        number of unsatisfied players (those with `satisfied is False`) by the
        total number of players.

        Returns:
            float: The output returned by the function `average_player_satisfaction`
            would be 0.

        """
        return len([p for p in self.players if p.satisfied is False]) / len(self.players)

    def get_average_and_max_player_luck(self):
        """
        This function calculates the average and maximum common player luck of a
        list of players and returns an object with the following properties:
        	- `average`: the average luck of all players
        	- `max`: the highest common player luck among all players
        	- `variance`: the variance of the luck values among all players

        Returns:
            dict: The output returned by the function is a dictionary with three
            key-value pairs:
            
            {"average": x / y; "max": z; "variance": w}
            
            where x is the total sum of all values from self.players[],
            y is the number of unique values observed among self.players[],
            z is the maximum value from res[key] among all players
            and
            w is the variance calculated based on x-average squared for each key.

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
        This function compares the satisfaction of players and captaincy minimums
        of two objects and returns a dictionary with the new score and old score.

        Args:
            other (): The `other` input parameter is passed as an instance of the
                same class as the one containing the method.

        Returns:
            dict: The output returned by the function is a dictionary with two
            keys: "new" and "old". The value of "new" is the score of the current
            object being compared (which is undefined), and the value of "old" is
            the score of the other object being compared (which is also undefined).

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
        The given function "log_unsatisfied_players" prints out the names of players
        who have not satisfied their game count.

        """
        for p in self.players:
            if p.satisfied == False:
                print(p.player_name, p.game_count)