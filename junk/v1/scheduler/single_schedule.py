from app.models.player import Player 
import statistics
from random import shuffle, choice, seed, random
from itertools import combinations
from .utils import *
from .gameslots import *
from .player import *

@log_timer
def init_histories(players):
    for player in players:
        for p in players:
                player.other_player_history[p.id] = 0
@log_timer
def get_histories(potential_game):
    sum_history = 0
    for player in potential_game:
        for p in potential_game:
                sum_history += player.other_player_history[p.id]
    return sum_history

@log_timer
def check_potential_game_length(potential_game, rules):
    return (len(potential_game) != rules)

@log_timer
def contains_high_game_count_player(potential_game, average_game_count):
    return any(player.game_count > average_game_count for player in potential_game)

@log_timer
def contains_players_already_scheduled(players_scheduled, potential_game):
    return any(player in players_scheduled for player in potential_game)

@log_timer
def player_fails_day_week_count(potential_game, day, week):
    for player in potential_game:
        day_count = player.days.count(day)
        week_count = player.weeks.count(week)
        if day_count >= player.rules['maxGamesDay'] or week_count >= player.rules['maxGamesWeek']:
            return True
    return False

@log_timer
def all_players_satisfied(potential_game):
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
    sum_history = 0
    for player in potential_game:
        for p in potential_game:
                sum_history += player.game_count
    return sum_history

def create_failure_scenarios():
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
    def recalculate_players(self):
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

    def get_average_game_count(self):
        return sum([p.game_count for p in self.players]) / len(self.players)
    
    def get_average_failure_count(self):
        return sum([abs(p.rules['minGamesTotal'] - p.game_count) for p in self.players]) / len(self.players)
    
    def average_player_satisfaction(self):
        return len([p for p in self.players if p.satisfied is False]) / len(self.players)

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