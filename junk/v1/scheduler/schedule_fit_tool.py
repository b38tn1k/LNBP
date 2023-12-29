from app.models import User, Club, Court, Flight, Player, Timeslot
import statistics
from random import shuffle, choice, seed, random
from itertools import combinations
from .utils import *
from .gameslots import *
from .player import *

        # leader = [
        #     good_candidates[0],
        #     good_candidates[0].get_average_and_max_player_luck(),
        # ]

        # min_max_common = leader[1]["max"]
        # for c in good_candidates:
        #     result = c.get_average_and_max_player_luck()
        #     if (
        #         result["max"] <= min_max_common
        #         and result["variance"] <= leader[1]["variance"]
        #         and result["average"] <= leader[1]["average"]
        #     ):
        #         leader = [c, result]
        #         min_max_common = result["max"]

class ScheduleFitTool:
    @log_timer
    def __init__(self, flight, template, gameslots):
        """
        This function appears to be a recipe or algorithm for generating a schedule
        of games for a set of players within a certain flight (or group) of players.
        It takes three arguments: `flight`, `template`, and `gameslots`, and it
        populates various attributes of the instance including `players`, `rules`,
        `gameslots`, and others.

        Args:
            flight (): The `flight` parameter passed into the `__init__` function
                of the `FlightScheduler` class contains information about a
                particular flight and is used to set various attributes within the
                scheduler object itself (e.g., `flight_id`, `rules`, `players`, etc.).
            template (dict): The `template` input parameter is a dictionary of
                default values for game attributes (such as court name and time
                slot) that are used to initialize the `Gameslot` objects when the
                `runCA` method is called.
            gameslots (list): The `gameslots` input parameter is a list of gameslots
                (time slots for matches) that are available for scheduling.

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
        self.run_sequence = [self.runCA,
                            self.pool_swaps,
                            self.sort_out_preferences,
                            self.sort_out_captains,
                            self.id_bad_timeslots,
                            self.segment_players_on_availability,
                            self.sort_unsatisfied_players,
                            self.increase_average_game_count,
                            self.sort_out_same_day_players,
                            self.shuffle_match,
                            self.clean_schedule,
                            self.add_entropy,
                            self.shuffle_match,
                            self.clean_schedule,
                            self.add_entropy,
                            self.pool_swaps,
                            self.sort_out_preferences,
                            self.sort_out_captains]
        
        self.run_sequence2 = [self.runCA,
                            self.sort_out_preferences,
                            self.sort_out_captains]
        
    @log_timer
    def runSF(self, toggle=True):
        """
        This function iterates over two lists of actions (`self.run_sequence` and
        `self.run_sequence2`) and performs the actions each iteration.

        Args:
            toggle (bool): The `toggle` input parameter is used to determine which
                sequence of actions (either `self.run_sequence` or `self.run_sequence2`)
                to run.

        """
        if toggle:
            for a in self.run_sequence:
                a()
                self.recalculate_players()
                if self.check_escape_conditions():
                    self.sort_out_preferences()
                    self.sort_out_captains()
                    print("ESCAPE!")
                    break
        else:
            for a in self.run_sequence2:
                a()
                self.recalculate_players()

    def check_escape_conditions(self):
        """
        This function checks if a list of players satisfy certain conditions related
        to their game schedules.

        Returns:
            bool: The output returned by this function is `True`.

        """
        for player in self.players:
            # players have min games
            if player.satisfied == False:
                return False
            # players aren't over scheduled
            if player.game_count > player.rules['maxGamesTotal']:
                return False
            for k in player.other_player_history:
                if player.other_player_history[k] >= 3:
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
                    return False
        return True

    def check_all_conditions(self):
        """
        This function checks if all conditions of a player are satisfied (i.e.,
        they have not played too many games on a single day or week), and returns
        True if all conditions are met and False otherwise.

        Returns:
            bool: The output returned by this function is `True`.

        """
        for player in self.players:
            if player.satisfied == False:
                return False
            if player.captain_count < player.rules["minCaptained"]:
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
        for game in self.gameslots:
            if game.full and game.captain is None:
                return False        
        return True

    @log_timer
    def runCA(self):
        """
        This function generates and schedules games for a set of players according
        to a set of rules and constraints. It uses a priority queue to select the
        most suitable games based on player availability and other game preferences.

        """
        def init_histories(players):
            """
            This function initializes the "other_player_history" dictionary for
            each player with the ID of the other players as keys and a value of 0.

            Args:
                players (list): The `players` input parameter is a list of players
                    that the function will loop over.

            """
            for player in players:
                for p in players:
                        player.other_player_history[p.id] = 0

        def get_histories(potential_game):
            """
            The function `get_histories` takes a list of players as an argument
            and returns the total history (a sum) of each player's interactions
            with all other players on the field.

            Args:
                potential_game (list): The `potential_game` input parameter is a
                    list of players and it is used to loop through each player's
                    history and calculate the total history for that player.

            Returns:
                int: The function `get_histories` takes a list of players
                `potential_game` as input and returns the sum of the history values
                of all possible pairs of players within the list.

            """
            sum_history = 0
            for player in potential_game:
                for p in potential_game:
                        sum_history += player.other_player_history[p.id]
            return sum_history
        
        def get_play_count(potential_game):
            """
            This function calculates the total number of plays that all players
            have made across all games of a "potential game".

            Args:
                potential_game (list): The `potential_game` input parameter is a
                    list of players and it allows the function to iterate through
                    all possible combinations of players for a given game.

            Returns:
                int: The output returned by this function is `0`.

            """
            sum_history = 0
            for player in potential_game:
                for p in potential_game:
                        sum_history += player.game_count
            return sum_history
        
        ts = set([g.timeslot_id for g in self.gameslots])
        tpp = {} # timeslot player pool
        for t in ts:
            tpp[t] = {}
            tpp[t]['all'] = [p for p in self.players if p.availability[t] != UNAVAILABLE]
            tpp[t]['filtered'] = [p for p in tpp[t]['all'] if p.availability[t] == AVAILABLE or (p.availability[t] == UNK and self.rules["assumeBusy"] is False)]
            tpp[t]['times'] = [g for g in self.gameslots if g.timeslot_id == t]
            tpp[t]['day'] = tpp[t]['times'][0].day_number
            tpp[t]['week'] = tpp[t]['times'][0].week_number
            tpp[t]['available_slots'] = len(tpp[t]['times'])
            tpp[t]['sgames'] = []
            tpp[t]['pgames'] = [] # all potential games
            game_grabber = tpp[t]['filtered'] if len(tpp[t]['filtered']) > self.rules["playersPerMatch"] else tpp[t]['all']
            if len(game_grabber) >= self.rules["playersPerMatch"]:
                for g in combinations(tpp[t]['all'], self.rules["playersPerMatch"]):
                    tpp[t]['pgames'].append(g)
        ts_list = list(ts)
        shuffle(ts_list)
        all_scheduled_games = []
        init_histories(self.players)
        total_players = len(self.players)
        total_games_added = 0
        while True:
            game_added = 0
            for t in ts_list:
                
                # Track which players have already been scheduled
                players_scheduled = set([p for p in [g for g in tpp[t]['sgames']]])
                
                # Track how many game slots we've filled for this timeslot
                slots_filled = 0
                
                # Game selection priority sorting
                sorted_games = sorted(tpp[t]['pgames'], key=lambda x: get_histories(x))

                already_added = False

                for potential_game in sorted_games:

                    if (len(potential_game) != self.rules['playersPerMatch']):
                        continue

                    if already_added:
                        break

                    # Apply Rule 1: Ensure we have available slots for this timeslot
                    if slots_filled >= tpp[t]['available_slots']:
                        # print("slots full")
                        break

                    if tpp[t]['available_slots'] == 0:
                        break

                    # Apply Rule 2: Check if any player in this game is already scheduled for this timeslot
                    if any(player in players_scheduled for player in potential_game):
                        # print("player scheduled")
                        continue

                    # Apply Rule 3: Count how many times the player has already played that day, week
                    failed_day_week_count = False
                    for player in potential_game:
                        day_count = player.days.count(tpp[t]['day'])
                        week_count = player.weeks.count(tpp[t]['week'])
                        if day_count >= player.rules['maxGamesDay'] or week_count >= player.rules['maxGamesWeek']:
                            failed_day_week_count = True
                            break
                    if failed_day_week_count is True:
                        # print("failed day or week count")
                        continue

                    # Apply Rule 4: Don't schedule games where all players have a game_count > tempRules["minGamesTotal"] 
                    # Apply Rule 5: Don't schedule games where any player has a game_count >= tempRules["maxGamesTotal"]
                    all_satisfied = True
                    over_scheduled = False

                    for player in potential_game:
                        if player.game_count < tempRules["minGamesTotal"]:
                            all_satisfied = False
                        if player.game_count >= tempRules["maxGamesTotal"]:
                            over_scheduled = True

                    if all_satisfied is True:
                        # print("failed satisfied count")
                        continue

                    if over_scheduled is True:
                        # print("failed max game count")
                        continue
                    
                    # All constraints satisfied, so we schedule this game
                    tpp[t]['sgames'].append(potential_game)
                    tpp[t]['available_slots'] -= 1
                    game_added += 1
                    total_games_added += 1

                    already_added = True

                    # Track all scheduled games also
                    all_scheduled_games.append(potential_game)
                    
                    # Update tracking variables
                    players_scheduled.update(potential_game)

                    slots_filled += 1

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
            if game_added == 0:
                break
            
        self.recalculate_players()
        for t in ts_list:
            if len(tpp[t]['sgames']) != 0:
                # tpp[t]['times']
                for i, sg in enumerate(tpp[t]['sgames']):
                    gs = tpp[t]['times'][i]
                    for p in sg:
                      gs.add_player_to_match(p)  

    def summarise_tests(self):
        """
        This function collects and returns various satisfaction-related values
        from the object's state.

        Returns:
            dict: The output returned by the function "summarise_tests" is a
            dictionary containing four key-value pairs:
            
            	- "all_players_satisfied": value determined by the "all_players_satisfied()"
            method
            	- "player_days_satisfied": value determined by the "player_days_satisfied()"
            method
            	- "player_weeks_satisfied": value determined by the "player_weeks_satisfied()"
            method
            	- "no_players_overscheduled": value determined by the
            "no_players_overscheduled()" method

        """
        result = {}
        result['all_players_satisfied'] = self.all_players_satisfied()
        result['player_days_satisfied'] = self.player_days_satisfied()
        result['player_weeks_satisfied'] = self.player_weeks_satisfied()
        result['no_players_overscheduled'] = self.no_players_overscheduled()
        return result

    def backup_gameslots(self):
        """
        The `backup_gameslots` function creates a copy of the game slots with their
        events attached.

        Returns:
            list: The output of the `backup_gameslots` function is a list `b`
            containing copies of all the elements of the original list `self.gameslots`,
            with each element being a copy of the corresponding game slot with its
            events appended.

        """
        b = []
        for g in self.gameslots:
            b.append(g.copy_with_events())
        return b

    def quick_log_game_count(self):
        """
        This function quick_log_game_count takes a player object and returns a
        string of all players' game counts concatenated together with spaces between
        them.

        Returns:
            str: The output returned by the function `quick_log_game_count` is an
            empty string "" (a none-string).

        """
        myString = ""
        for p in self.players:
            myString += str(p.game_count) + " "
        # print(myString)
        return myString.strip()

    def segment_players_on_availability(self):
        """
        This function takes a list of players and calculates the mean availability
        score of the list.

        """
        mean_score = statistics.mean(
            [player.availability_score for player in self.players]
        )
        for player in self.players:
            player.set_availability_score_relation(mean_score)
            # print(player.availability_score_greater_than_mean)

    def id_bad_timeslots(self):
        """
        This function checks which timeslots are underutilized and marks them as
        bad for the purpose of availability calculation.

        """
        gts = {}
        for p in self.players:
            for a in p.availability:
                if p.availability[a] != UNAVAILABLE:
                    if a in gts:
                        gts[a] += 1
                    else:
                        gts[a] = 1
        bad_ts = []
        for k in gts:
            if gts[k] < self.rules['playersPerMatch'] * (1.0 / self.rules['minimumSubsPerGame']):
                bad_ts.append(k)
        to_remove = [g for g in self.gameslots if g.timeslot_id in bad_ts]
        for r in to_remove:
            r.good_availability = False
            # self.gameslots.remove(r)

    def check_test(self):
        """
        The function "check_test" checks for availability of players for each game
        slot and adds them to the list of games if they are available.

        """
        for g in self.gameslots:
            for p in self.players:
                if p.availability[g.timeslot_id] != UNAVAILABLE:
                    g.game_event.append(p)
                    print("add")
        self.recalculate_players()
        self.create_events(skip=True)
        self.recalculate_players()

    def increase_average_game_count(self):
        """
        This function increases the average game count of players and redistributes
        them to fill available slots while ensuring that no player is over-matched
        or under-matched.

        """
        average = sum([player.game_count for player in self.players]) / len(self.players)
        at_risk = [player for player in self.players if player.game_count < average]
        for p in at_risk:
            candidates = [g for g in self.gameslots if g.full is False]
            filtered = [c for c in candidates if c.is_building_already()]
            for ts in filtered:
                    ts.add_player_to_match(p)
                    self.recalculate_players()
            for ts in candidates:
                    ts.add_player_to_match(p)
                    self.recalculate_players()
        candidates = [g for g in self.gameslots if g.full is False]
        filtered = [c for c in candidates if c.is_building_already()]
        for p in self.players:
            for ts in filtered:
                    ts.add_player_to_match(p)
                    self.recalculate_players()
            for ts in candidates:
                    ts.add_player_to_match(p)
                    self.recalculate_players()

    def sort_out_same_day_players(self):
        """
        This function sorts out players for the same day's games based on their
        availability and fills up available game slots with suitable players.

        """
        players, days = self.get_player_days_unsatisfied()
        for p in players:
            left_overs = []
            j = 1
            for g in days[p.id][j:]: # keep the first game
                if not isinstance(g, list):
                    for lo in g.game_event:
                        if lo not in players:
                            left_overs.append(lo)
                    g.game_event = []
            if len(left_overs) > self.rules['playersPerMatch']:
                days[p.id][j] = left_overs[:self.rules['playersPerMatch']]
        self.recalculate_players()


    def force_match(self):
        """
        This function "force_match" takes a list of unsatisfied players (i.e.,
        those who are not yet assigned to any match), and tries to find matches
        for them by iterating through available gameslots and matching the players
        with the games. It updates the "filtered" dictionary with the games that
        were matched and removes the corresponding gameslots from the availability
        dict. If there are no more games available for a particular player
        satisfaction of "Unsatisfied", it deletes that key from the "filtered" dictionary.

        """
        self.recalculate_players()
        bad_players = [p for p in self.players if p.satisfied == False]
        avail = {}
        for p in bad_players:
            for ts in p.availability:
                if p.availability[ts] != UNAVAILABLE:
                    if ts in avail:
                        avail[ts].append(p)
                    else:
                        avail[ts] = [p]
        filtered = {}
        # to_delete = []
        for k in avail:
            filtered[k] = {}
            filtered[k]['games'] = [g for g in self.gameslots if g.full == False and g.timeslot_id == k]
            for g in filtered[k]['games']:
                filtered[k]['players'] = []
                for p in avail[k]:
                    if g.hypothetically_player_can_be_added(p):
                        filtered[k]['players'].append(p)
        #         if len(filtered[k]['players']) < 1:
        #             to_delete.append(k)
        # for k in to_delete:
        #     del filtered[k]
        for k in filtered:
            games = filtered[k]['games']
            for g in games:
                ps = self.get_appropriate_players(g, filtered[k]['players'])
                if len(ps) == self.rules['playersPerMatch']:
                    for p in ps:
                        g.add_player_to_match(p)
                    self.force_match()
    
    def get_appropriate_players(self, game, desperates):
        """
        This function returns a list of appropriate players for a match based on
        the following conditions:
        1/ The number of desperation moves (i.e., players who are already known
        to be playing) is not more than the maximum number of players allowed per
        match.
        2/ If there are fewer than the maximum number of players allowed per match
        among the desperation moves list), the function returns those players.
        3/ If there are not enough desperation moves to reach the maximum number
        of players allowed per match and some players have already played their
        first move (hypothetically speaking), the function adds those players to
        the candidates list for consideration.

        Args:
            game (): The `game` input parameter is used to determine which players
                are eligible for selection based on the game's current state.
            desperates (list): The `desperates` input parameter is a list of players
                who have already been chosen for the game.

        Returns:
            list: The output returned by this function is a list of up to
            `self.rules['playersPerMatch']` players selected from the `desperates`
            list and the `self.players` list based on the conditions mentioned.

        """
        if len(desperates) >= self.rules['playersPerMatch']:
            return desperates[:self.rules['playersPerMatch']]
        candidates = []
        for p in self.players:
            if not p in desperates:
                if game.hypothetically_player_can_be_added(p):
                    candidates.append(p)
        return candidates

    def clear_everything(self):
        """
        This function clears all the game slots and their events and full states
        of a list of gameslots belonging to an object of an unspecified class.

        """
        for g in self.gameslots:
            g.game_event = []
            g.full = False
        self.recalculate_players()

    def print_problems(self, res):
        """
        This function prints the names of the players who are facing problems
        during game play.

        Args:
            res (dict): The `res` input parameter is a list of dictionaries
                representing game results.

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
    def pool_swaps(self):
        """
        This function is a loop that attempts to optimize the players' luck by
        doing easy swaps until a certain condition is met or a maximum number of
        attempts is reached.

        """
        self.recalculate_players()
        backup = self.get_average_and_max_player_luck()
        if backup["max"] == 1:
            return
        backup["b"] = self.backup_gameslots()
        for i in range(ATTEMPTS):
            count = self.do_easy_swaps()
            if count == 0:
                break
            self.recalculate_players()
            res = self.get_average_and_max_player_luck()
            # if res['average'] <= backup['average'] and res['max'] <= backup['max']:
            if res["variance"] <= backup["variance"] and res["max"] <= backup["max"]:
                backup = res
                backup["b"] = self.backup_gameslots()
                if res["max"] == 2:
                    break
        self.gameslots = backup["b"]

    @log_timer
    def get_potential_swaps(self):
        """
        This function identifies potential swaps of players between games that
        have overlapping players and have not yet been matched with a swap.

        Returns:
            dict: The output returned by this function is a list of tuples named
            "potential_swaps" which contains tuples with attributes: "_og", "_op",
            "g" and "p".

        """
        res = self.get_problem_players_and_games()
        potential_swaps = []

        # Convert game_events of each gameslot into a set
        gameslots_events_as_sets = [set(g.game_event) for g in self.gameslots]

        for r in res:
            r_players_set = set(r["players"])

            # This is now a generator
            filtered_gameslots = (
                g
                for g, event_set in zip(self.gameslots, gameslots_events_as_sets)
                if not r_players_set & event_set
            )

            r_game = r["game"]
            r_game_get_players_available_to_swap = r_game.get_players_available_to_swap

            for g in filtered_gameslots:
                op = g.get_players_available_to_swap(r_game)
                pp_set = r_players_set & set(r_game_get_players_available_to_swap(g))

                to_remove = []
                for p in pp_set:
                    if g.week_number in p.weeks:
                        to_remove.append(p)
                for p in to_remove:
                    pp_set.remove(p)
                to_remove = []
                for p in op:
                    if r_game.week_number in p.weeks:
                        to_remove.append(p)
                for p in to_remove:
                    op.remove(p)

                if op and pp_set:
                    ps = {"_og": g, "_op": list(op), "g": r_game, "p": list(pp_set)}
                    potential_swaps.append(ps)

        return potential_swaps

    @log_timer
    def find_best_swaps(self, potential_swaps):
        """
        This function takes a list of potential swaps (dictionaries containing the
        player making the swap and the game they are swapping into), and returns
        a dictionary mapping player IDs to information about the best swaps for
        each player.

        Args:
            potential_swaps (dict): The `potential_swaps` input parameter is a
                list of dictionaries containing information about potential swaps
                (player ID from old game to player ID of new game) and their
                corresponding deltas.

        Returns:
            dict: The function `find_best_swaps` returns a dictionary of potential
            player swaps between two games.

        """
        swaps = {}

        for s in potential_swaps:
            _og = s["_og"]
            game = s["g"]
            _og_calculate_history_delta = _og.calculate_history_delta
            game_calculate_history_delta = game.calculate_history_delta

            for op in s["_op"]:
                for p in s["p"]:
                    # the delta of the old player in the old game + the player in the game
                    old_delta = _og_calculate_history_delta(
                        op, p
                    ) + game_calculate_history_delta(p, op)

                    # the delta of the player in the old game + the old player in the game
                    new_delta = _og_calculate_history_delta(
                        p, op
                    ) + game_calculate_history_delta(op, p)
                    delta = old_delta - new_delta

                    existing_swap = swaps.get(p.id)
                    if existing_swap:
                        if delta > existing_swap["delta"]:
                            existing_swap["delta"] = delta
                            existing_swap["g"] = game
                            existing_swap["_og"] = _og
                            existing_swap["p"] = p
                            existing_swap["_op"] = op
                    else:
                        swaps[p.id] = {
                            "g": game,
                            "_og": _og,
                            "p": p,
                            "_op": op,
                            "delta": delta,
                        }

        return swaps

    @log_timer
    def do_easy_swaps(self):
        """
        This function implements a simple swap algorithm to move gametic events
        from one player's game event set to another player's set.

        Returns:
            int: The output returned by this function is a single integer value
            representing the number of swaps made.

        """
        potential_swaps = self.get_potential_swaps()
        if len(potential_swaps) == 0:
            return 0
        swaps = self.find_best_swaps(potential_swaps)
        if len(swaps) == 0:
            return 0
        count = 0
        swapped = []
        for s in swaps:
            swap = swaps[s]
            _og_game_event = set(swap["_og"].game_event)
            g_game_event = set(swap["g"].game_event)

            if swap["_op"] in _og_game_event and swap["p"] in g_game_event:
                _og_game_event.remove(swap["_op"])
                g_game_event.remove(swap["p"])
                g_game_event.add(swap["_op"])
                _og_game_event.add(swap["p"])
                count += 1
                swapped.append(swap["p"].id)
                swapped.append(swap["_op"].id)

            swap["_og"].game_event = list(_og_game_event)
            swap["g"].game_event = list(g_game_event)
        return count

    @log_timer
    def get_problem_players_and_games(self):
        """
        This function identifies problem players and games with unsatisfied days
        (OD) for a given list of players and games. It first calculates the maximum
        common count of a player's preferred days across all games they are part
        of and selects the player with the highest common count as the most
        consistent player. The function then loops through each game and calculates
        the number of problem players for each event day.

        Returns:
            dict: The output of this function is a list of dictionaries each
            containing information about a problematic game and the players involved.
            Each dictionary has three keys: "game", "players", and "coupled". The
            "game" key refers to the specific game instance being described. The
            "players" key contains an iteratorable of one or more player objects
            (which might have more than one player involved) for the game with no
            other solutions for swappable player slots.

        """
        max_common = 0
        problem_players = []
        # Single loop over players to find max_common and problem_players
        player_common_counts = {}
        for p in self.players:
            res = p.get_most_common_player_and_count()
            player_common_counts[p] = res
            local_max = max(res.values(), default=0)
            if local_max > max_common:
                max_common = local_max
                problem_players = [p]
            elif local_max == max_common:
                problem_players.append(p)

        # Find problem games
        problem_games = []
        
        for e in self.gameslots:
            count_problem_players = len(set(problem_players) & set(e.game_event))
            if count_problem_players >= 2:
                problem_games.append(e)
        # find double up players / the other swappable problem
        odp, odg = self.get_player_days_unsatisfied()
        more_problem_games = set()
        for i in odp:
            for k in odg[i.id]:
                more_problem_games.add(k)
        for p in odp:
            problem_players.append(p)
        for g in more_problem_games:
            problem_games.append(g)

        # Couple games with problem players
        coupled = []
        for g in problem_games:
            game_event_set = set(g.game_event)
            coupled.append(
                {
                    "game": g,
                    "players": [p for p in problem_players if p in game_event_set],
                }
            )

        return coupled

    @log_timer
    def recalculate_players(self):
        """
        This function recalculates the satisfaction level of each player based on
        their current games and history with other players.

        """
        satisfied = {}
        for p in self.players:
            satisfied[p.id] = 0
            p.days = []
            p.weeks = []
            p.captain_count = 0
            p.game_count = 0
            for k in p.other_player_history:
                p.other_player_history[k] = 0
        for game in self.gameslots:
            if game.full:
                for p in game.game_event:
                    if game.captain:
                        if p == game.captain:
                            p.captain_count += 1
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

    @log_timer
    def sort_out_captains(self, count=0):
        """
        This function sorts out the captains of games played by players registered
        to a league instance.

        Args:
            count (int): The `count` input parameter is an optional integer that
                specifies the number of attempts to assign captains to gameslots.
                If all players have not been assigned as captain at least the
                minimum number of times after `count` attempts are made (i.e.,
                `self.all_players_captained_minimum()==False`), the function will
                recalculate players and repeat the process (calling itself with
                `count + 1`).

        """
        players_to_assign = list(self.players)
        shuffle(players_to_assign)
        for game in self.gameslots:
            if game.full:
                if players_to_assign:
                    potential_captains = [
                        player for player in players_to_assign if player in game.game_event and player.captain_count < player.rules['minCaptained']
                    ]
                    if potential_captains:
                        captain = potential_captains.pop(0)
                        players_to_assign.remove(captain)
                        game.captain = captain
                if game.captain is None:    
                    game.captain = choice(game.game_event)
                game.captain.captain_count += 1
        if not self.all_players_captained_minimum() and count < ATTEMPTS:
            for game in self.gameslots:
                game.captain = None
            self.recalculate_players()
            self.sort_out_captains(count + 1)

        # if players_to_assign:
        #     print(f"Warning: {len(players_to_assign)} players couldn't be assigned as captain the minimum number of times.")

    @log_timer
    def add_entropy(self):
        # Compute full_slots once outside the loop
        """
        This function takes a list of "slot" objects as input and adds entropy to
        the list by repeatedly swapping one random full slot with another random
        empty slot.

        """
        full_slots = [
            slot
            for slot in self.gameslots
            if slot.full == True or slot.is_building_already() == True
        ]

        # If there's only one or no full slot, exit
        if len(full_slots) <= 1:
            return

        full_slot_ids = {slot.timeslot_id for slot in full_slots}

        for i in range(200):
            gs = choice(full_slots)

            # Use a set to quickly find a different ogs
            other_ids = full_slot_ids - {gs.timeslot_id}
            ogs_timeslot_id = choice(list(other_ids))
            ogs = next(
                slot for slot in full_slots if slot.timeslot_id == ogs_timeslot_id
            )

            gs.try_exchange(ogs)

    def get_days(self):
        """
        This function returns a dictionary of day numbers to lists of GameSlot
        objects that are fully booked on those days.

        Returns:
            dict: The output returned by this function is a dictionary of day
            numbers to lists of game slots that are full on that day.

        """
        full_slots = [slot for slot in self.gameslots if slot.full == True]
        days = {}
        for slot in full_slots:
            if slot.day_number in days:
                days[slot.day_number].append(slot)
            else:
                days[slot.day_number] = [slot]
        return days

    def swap_player_to_game(self, player, src_game, dst_game):
        """
        This function swaps a player from one game to another.

        Args:
            player (): The `player` input parameter is the player object that needs
                to be swapped from one game to another.
            src_game (): The `src_game` input parameter is used to identify the
                game from which the player being swapped is currently assigned.
            dst_game (): The `dst_game` input parameter specifies the game to which
                the player will be swapped.

        """
        dst_player = dst_game.get_swap_candidate_player()
        if dst_player.availability[src_game.timeslot_id] == AVAILABLE:
            dst_game.remove_player_from_match(dst_player)
            src_game.remove_player_from_match(player)
            src_game.add_player_to_match(dst_player)
            dst_game.add_player_to_match(player)

    def decide_how_to_swap(self, player, src_game, dst_game):
        """
        This function decides whether to swap two games or a player between two
        games based on availability.

        Args:
            player (): The `player` input parameter specifies which player is being
                swapped.
            src_game (): The `src_game` input parameter specifies the game that
                the player is currently playing and whose availability we are
                checking for swapping purposes.
            dst_game (): The `dst_game` parameter specifies the game slot that the
                player will be swapped to.

        """
        perfect_swap = True
        for p in src_game.game_event:
            perfect_swap = p.availability[dst_game.timeslot_id] == AVAILABLE
            if not perfect_swap:
                break
        if perfect_swap:
            for game in self.gameslots:
                if (game.timeslot_id == dst_game.timeslot_id) and not game.full:
                    self.swap_whole_game(src_game, dst_game)
                    return
            for p in dst_game.game_event:
                perfect_swap = p.availability[src_game.timeslot_id] == AVAILABLE
                if not perfect_swap:
                    break
        if perfect_swap:
            self.swap_whole_game(src_game, dst_game)
        else:
            self.swap_player_to_game(player, src_game, dst_game)

    def swap_whole_game(self, src, dst):
        """
        This function swaps two player lists (src and dst) within a match. It first
        copies the player list from src to a temporary list s and removes the
        players from src's game event. Then it copies the player list from dst to
        another temporary list d and removes the players from dst's game event.
        After that it adds the players from s back into src's game event and adds
        the players from d back into dst's game event.

        Args:
            src (): The `src` input parameter is the game object that we want to
                swap players from.
            dst (): The `dst` input parameter is a copy of the `src` input parameter.

        """
        s = []
        for p in src.game_event:
            s.append(p)
            src.remove_player_from_match(p)
        d = []
        for p in dst.game_event:
            d.append(p)
            dst.remove_player_from_match(p)
        for p in s:
            src.add_player_to_match(p)
        for p in d:
            dst.add_player_to_match(p)

    @log_timer
    def sort_out_preferences(self):
        """
        This function sorts out the player's preferences by iterating through the
        games on each day and selecting the best game for each player based on
        their availability and preferences.

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
    def shuffle_match(self):
        # print(len(self.gameslots))
        # Filter players based on the new property
        """
        This function shuffles the players and game slots to create a schedule for
        a sport league. It first filters the players based on their availability
        score and then iteratively matches the players with the available game
        slots until all games are filled.

        """
        less_than_mean = [
            player
            for player in self.players
            if not player.availability_score_greater_than_mean
        ]
        greater_than_mean = [
            player
            for player in self.players
            if player.availability_score_greater_than_mean
        ]

        for i in range(self.rules["minGamesTotal"]):
            self.match_schedule()
            self.recalculate_players()
            shuffle(greater_than_mean)

            # Update players list
            self.players = less_than_mean.copy()
            self.players.extend(greater_than_mean)

            shuffle(self.gameslots)
            self.gameslots.sort(key=lambda gs: gs.court_name, reverse=True)

        # for e in [g for g in self.gameslots if len(g.game_event) >= 4]:
        #     print(len(e.game_event))
        # print(len(self.gameslots))
        self.tidy_schedule()

    def clean_schedule(self):
        # count = len([g for g in self.gameslots if len(g.game_event) > 0])
        # deep_clean = count > len(self.players)
        """
        This function cleans up the game schedule by removing completed games and
        players who are no longer needed.

        """
        for gs in self.gameslots:
            self.recalculate_players()
            if gs.full:
                gs.self_destruct_if_unneccessary()
            self.recalculate_players()
            gs.self_destruct_if_incomplete()

    def tidy_schedule(self):
        """
        This function calls `recalculate_players` and then iterates over all
        `Gameslot` objects associated with the current object (`gs`) and calls
        their `self_destruct_if_incomplete` method if they are incomplete.

        """
        self.recalculate_players()
        for gs in self.gameslots:
            gs.self_destruct_if_incomplete()

    def trim_schedule(self):
        """
        The `trim_schedule` function removes any full game slots (GS) from the
        schedule and destroys them if unnecessary.

        """
        self.recalculate_players()
        for gs in self.gameslots:
            if gs.full:
                gs.self_destruct_if_unneccessary()

    @log_timer
    def sort_unsatisfied_players(self):
        """
        This function sorts the list of unsatisfied players based on their
        availability scores and assigns them to games according to their preferences
        and availability.

        """
        remainders = [player for player in self.players if not player.satisfied]
        remainders = sorted(remainders, key=lambda player: player.availability_score)
        avails = []
        for gs in self.gameslots:
            if gs.full:
                temp_dict = {}
                temp_dict["game"] = gs
                temp_dict["players"] = []
                for player in remainders:
                    if player.check_game_availability(gs) == True:
                        temp_dict["players"].append(player)
                avails.append(temp_dict)
        avails = sorted(
            avails,
            key=lambda a_dict: a_dict["game"].get_total_availability_score(),
            reverse=True,
        )
        j = 0
        # displaced = []
        if len(remainders) != 0:
            for a_dict in avails:
                player = remainders[j % len(remainders)]
                if player.game_count < player.rules["minGamesTotal"] and a_dict[
                    "game"
                ].hypothetically_player_can_be_added(player):
                    swapped_player = a_dict["game"].swap_in(player)
                    self.recalculate_players()
                    # displaced.append(player)
                j += 1


    @log_timer
    def preliminary_schedule_match(self):
        """
        This function matches players with available gameslots to form a preliminary
        schedule for the players.

        """
        for player in [p for p in self.players if not p.availability_score_greater_than_mean]:
            all_options = [g for g in self.gameslots if g.player_can_be_added(player)]
            candidates = [gameslot for gameslot in all_options if gameslot.is_building_already() and not gameslot.full is True]
            if candidates:
                for c in candidates:
                    c.add_player_to_match(player)
            for c in [c for c in all_options if c not in candidates]:
                c.add_player_to_match(player)
            self.recalculate_players()

    @log_timer
    def match_schedule(self):
        """
        This function iterates over the list of players and matches each player
        with available game slots to create a match.

        """
        for player in self.players:
            all_options = [g for g in self.gameslots if g.player_can_be_added(player) and g.full is False and not player in g.game_event]
            filtered_options = [g for g in all_options if g.good_availability  and g.full is False]
            candidates = [
                gameslot for gameslot in all_options if gameslot.is_building_already() and gameslot.full is False
            ]

            # Check if candidates or all_options are available and pop from the list
            game_slot_to_add = None
            if candidates:
                game_slot_to_add = candidates.pop()
            elif filtered_options:
                game_slot_to_add = filtered_options.pop()
            elif all_options:
                game_slot_to_add = all_options.pop()
            if game_slot_to_add:
                self.recalculate_players()
                game_slot_to_add.add_player_to_match(player)
                self.recalculate_players()

    @log_timer
    def create_events(self, skip=False):
        """
        This function creates a game event for each gameslot object that is either
        full or has a skip value of True.

        Args:
            skip (bool): The `skip` input parameter is a optional paramether that
                if set to True will skip creating events for gameslots with the
                full status

        """
        for gameslot in self.gameslots:
            if gameslot.full is True or skip is True:
                # def create_event(self, court, players):
                # timeslot = self.flight_obj.get_timeslot_by_id(gameslot.timeslot_id)
                # court = timeslot.get_court_by_id(gameslot.court_id)
                timeslot = gameslot.timeslot_obj
                court = gameslot.court_obj
                captain = None
                if gameslot.captain:
                    captain = self.flight_obj.get_players_by_id(gameslot.captain.id)
                players = []
                for player in gameslot.game_event:
                    players.append(self.flight_obj.get_players_by_id(player.id))
                timeslot.create_event(court, players, captain)

    def all_players_satisfied(self):
        """
        The function `all_players_satisfied` checks whether all players included
        as instances of `player` (the class or type of objects stored within the
        container called `self.players`) satisfy the condition `satisfied = False`.
        If a player is not satisfied (i.e., their condition is not False), then
        the function returns False. However—and since the loop checks all players'
        conditions—if every player has its satisfied attribute set to False (i.e.,
        no player is not satisfied), the function returns True indicating all
        players are indeed happy or pleased.

        Returns:
            bool: The output returned by this function is `True`.

        """
        for player in self.players:
            if player.satisfied == False:
                return False
        return True
    
    def no_players_overscheduled(self):
        """
        This function checks whether any of the players are overscheduled by
        comparing their game count to the maximum number of games allowed for each
        player according to their rules.

        Returns:
            bool: The output returned by the function "no_players_overscheduled"
            is "True".

        """
        for player in self.players:
            if player.game_count > player.rules['maxGamesTotal']:
                return False
        return True

    def player_days_satisfied(self):
        """
        This function checks whether a list of players has played too many games
        on any one day within the specified "maxGamesDay" limit. It iterates through
        each player and checks if they have exceeded the maximum number of games
        allowed per day by checking if the number of games played on that day is
        greater than the specified limit. If any player has exceeded the limit
        then the function returns False.

        Returns:
            bool: The output returned by this function is `True`.

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
        This function checks whether any player has played more than the maximum
        number of games allowed per week for all the weeks they have played so far.

        Returns:
            bool: The output returned by this function is "True".

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
        This function retrieves a list of players and their corresponding unsatisfied
        days (days where they have more games than the maximum allowed).

        Returns:
            dict: The output returned by this function is a tuple containing two
            items:
            
            1/ A list of players (called "us") who have unsatisfied days (i.e.,
            days with more games than the maximum allowed by their rules).
            2/ A dictionary (called "bg") that maps each player ID to a list of
            games played on the specific day that has too many games.

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
        This function finds all games on a given day that involve a specific player.
        It loops through a list of game slots and checks if the player is present
        as an event participant.

        Args:
            player (str): The `player` input parameter filters the games that are
                returned based on whether or not they contain the given player as
                a participant.
            day (int): The `day` input parameter specifies the date for which games
                are to be searched for.

        Returns:
            list: The function "find_games_on_day_with_player" takes two arguments:
            player and day.

        """
        res = []
        for g in [g for g in self.gameslots if g.day_number == day]:
            if player in g.game_event:
                res.append(g)
        return res
    
    def log_player_days_unsatisfied(self):
        """
        This function retrieves the player days unsatisfied and prints the player
        names and start times of the events that took place on those days.

        """
        p, d = self.get_player_days_unsatisfied()
        for i in p:
            print(i.player_name)
            for k in d[i.id]:
                print(k.start_time)
            print()

    def get_gameslots_by_day(self, day_number):
        """
        This function retrieves a list of `gameslot` objects from a list
        `self.gameslots` that have a `day_number` matching the provided `day_number`
        argument.

        Args:
            day_number (int): The `day_number` input parameter specifies which
                day's gameslots the function should return.

        Returns:
            list: The output returned by this function is a list of gameslots.

        """
        return [
            gameslot for gameslot in self.gameslots if gameslot.day_number == day_number
        ]

    def get_gameslots_by_week(self, week_number):
        """
        The function "get_gameslots_by_week" takes a "week_number" parameter and
        returns a list of gameslots that have the specified week number.

        Args:
            week_number (int): The `week_number` input parameter specifies the
                desired week for which the function should return the corresponding
                game slots.

        Returns:
            list: The function "get_gameslots_by_week" returns a list of gameslots
            that have a week number equal to the input "week_number".

        """
        return [
            gameslot
            for gameslot in self.gameslots
            if gameslot.week_number == week_number
        ]

    def log(self, dofilter=False):
        """
        This function logs data from all players and gameslots within an instance
        of the object it's a method of.

        Args:
            dofilter (int): The `dofilter` parameter is passed to each object's
                `log()` method as a truthy value (True) if it should filter its
                output log statements or False otherwise.

        """
        for p in self.players:
            p.log(dofilter)
        for gs in self.gameslots:
            gs.log(dofilter)

    def all_players_captained_minimum(self):
        """
        This function checks whether all players on a team have reached the minimum
        number of games captained as specified by their rules.

        Returns:
            bool: The output returned by the function is "True".

        """
        for p in self.players:
            if p.captain_count < p.rules["minCaptained"]:
                return False
        return True
    
    def log_players_captained_minimum(self):
        """
        The function `log_players_captained_minimum` logs the player names of those
        who have captained a minimum number of games according to their rules.

        """
        for p in self.players:
            if p.captain_count < p.rules["minCaptained"]:
                print(p.player_name)

    def all_games_captained(self):
        """
        This function checks if all games slots have a player as captain or not.

        Returns:
            bool: The output returned by this function is `True`.

        """
        for g in self.gameslots:
            if g.full == True and g.captain is None:
                return False
        return True

    def get_average_and_max_player_luck(self):
        """
        This function calculates the average and maximum common luck of a set of
        players.

        Returns:
            dict: The output returned by this function is a dictionary containing
            three variables:
            
            	- "average": the average of all the player luck values
            	- "max": the maximum player luck value
            	- "variance": the variance of all the player luck values

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
        This function compares two objects (presumably representing player lists)
        and returns a dictionary containing the scores based on two satisfaction
        criteria: all players satisfied and all players captained minimally.

        Args:
            other (): The `other` parameter is the object being compared to the
                instance of the class that the function is a part of.

        Returns:
            dict: The output returned by the function `compare_basics` is a
            dictionary with two keys: "new" and "old".

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
        The given function prints the player names and game counts of players who
        are not satisfied (i.e., their `satisfied` attribute is `False`).

        """
        for p in self.players:
            if p.satisfied == False:
                print(p.player_name, p.game_count)