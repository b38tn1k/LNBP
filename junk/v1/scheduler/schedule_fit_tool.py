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
        def init_histories(players):
            for player in players:
                for p in players:
                        player.other_player_history[p.id] = 0

        def get_histories(potential_game):
            sum_history = 0
            for player in potential_game:
                for p in potential_game:
                        sum_history += player.other_player_history[p.id]
            return sum_history
        
        def get_play_count(potential_game):
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
        result = {}
        result['all_players_satisfied'] = self.all_players_satisfied()
        result['player_days_satisfied'] = self.player_days_satisfied()
        result['player_weeks_satisfied'] = self.player_weeks_satisfied()
        result['no_players_overscheduled'] = self.no_players_overscheduled()
        return result

    def backup_gameslots(self):
        b = []
        for g in self.gameslots:
            b.append(g.copy_with_events())
        return b

    def quick_log_game_count(self):
        myString = ""
        for p in self.players:
            myString += str(p.game_count) + " "
        # print(myString)
        return myString.strip()

    def segment_players_on_availability(self):
        mean_score = statistics.mean(
            [player.availability_score for player in self.players]
        )
        for player in self.players:
            player.set_availability_score_relation(mean_score)
            # print(player.availability_score_greater_than_mean)

    def id_bad_timeslots(self):
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
        for g in self.gameslots:
            for p in self.players:
                if p.availability[g.timeslot_id] != UNAVAILABLE:
                    g.game_event.append(p)
                    print("add")
        self.recalculate_players()
        self.create_events(skip=True)
        self.recalculate_players()

    def increase_average_game_count(self):
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
        if len(desperates) >= self.rules['playersPerMatch']:
            return desperates[:self.rules['playersPerMatch']]
        candidates = []
        for p in self.players:
            if not p in desperates:
                if game.hypothetically_player_can_be_added(p):
                    candidates.append(p)
        return candidates

    def clear_everything(self):
        for g in self.gameslots:
            g.game_event = []
            g.full = False
        self.recalculate_players()

    def print_problems(self, res):
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
        full_slots = [slot for slot in self.gameslots if slot.full == True]
        days = {}
        for slot in full_slots:
            if slot.day_number in days:
                days[slot.day_number].append(slot)
            else:
                days[slot.day_number] = [slot]
        return days

    def swap_player_to_game(self, player, src_game, dst_game):
        dst_player = dst_game.get_swap_candidate_player()
        if dst_player.availability[src_game.timeslot_id] == AVAILABLE:
            dst_game.remove_player_from_match(dst_player)
            src_game.remove_player_from_match(player)
            src_game.add_player_to_match(dst_player)
            dst_game.add_player_to_match(player)

    def decide_how_to_swap(self, player, src_game, dst_game):
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
        for gs in self.gameslots:
            self.recalculate_players()
            if gs.full:
                gs.self_destruct_if_unneccessary()
            self.recalculate_players()
            gs.self_destruct_if_incomplete()

    def tidy_schedule(self):
        self.recalculate_players()
        for gs in self.gameslots:
            gs.self_destruct_if_incomplete()

    def trim_schedule(self):
        self.recalculate_players()
        for gs in self.gameslots:
            if gs.full:
                gs.self_destruct_if_unneccessary()

    @log_timer
    def sort_unsatisfied_players(self):
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
        for player in self.players:
            if player.satisfied == False:
                return False
        return True
    
    def no_players_overscheduled(self):
        for player in self.players:
            if player.game_count > player.rules['maxGamesTotal']:
                return False
        return True

    def player_days_satisfied(self):
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
        res = []
        for g in [g for g in self.gameslots if g.day_number == day]:
            if player in g.game_event:
                res.append(g)
        return res
    
    def log_player_days_unsatisfied(self):
        p, d = self.get_player_days_unsatisfied()
        for i in p:
            print(i.player_name)
            for k in d[i.id]:
                print(k.start_time)
            print()

    def get_gameslots_by_day(self, day_number):
        return [
            gameslot for gameslot in self.gameslots if gameslot.day_number == day_number
        ]

    def get_gameslots_by_week(self, week_number):
        return [
            gameslot
            for gameslot in self.gameslots
            if gameslot.week_number == week_number
        ]

    def log(self, dofilter=False):
        for p in self.players:
            p.log(dofilter)
        for gs in self.gameslots:
            gs.log(dofilter)

    def all_players_captained_minimum(self):
        for p in self.players:
            if p.captain_count < p.rules["minCaptained"]:
                return False
        return True
    
    def log_players_captained_minimum(self):
        for p in self.players:
            if p.captain_count < p.rules["minCaptained"]:
                print(p.player_name)

    def all_games_captained(self):
        for g in self.gameslots:
            if g.full == True and g.captain is None:
                return False
        return True

    def get_average_and_max_player_luck(self):
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
        other_score = 0
        self_score = 0

        other_score += other.all_players_satisfied()
        other_score += other.all_players_captained_minimum()

        self_score += self.all_players_satisfied()
        self_score += self.all_players_captained_minimum()
        return {"new": self_score, "old": other_score}
    
    def log_unsatisfied_players(self):
        for p in self.players:
            if p.satisfied == False:
                print(p.player_name, p.game_count)