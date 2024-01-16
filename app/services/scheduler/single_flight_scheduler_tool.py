from random import shuffle
from itertools import combinations
from .constants import *


def init_histories(players):
    print("Init Histories")
    for player in players:
        for p in players:
            player.other_player_history[p.id] = 0


def get_histories(potential_game):
    sum_history = 0
    for player in potential_game:
        for p in potential_game:
            sum_history += player.other_player_history[p.id]
    return sum_history


def check_potential_game_length(potential_game, rules):
    return len(potential_game) != rules


def contains_high_game_count_player(potential_game, average_game_count):
    return any(player.game_count > average_game_count for player in potential_game)


def contains_players_already_scheduled(players_scheduled, potential_game):
    return any(player in players_scheduled for player in potential_game)


def player_fails_day_week_count(potential_game, day, week):
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
    all_satisfied = True
    over_scheduled = False
    for player in potential_game:
        if player.game_count < player.rules["min_games_total"]:
            all_satisfied = False
        if player.game_count >= player.rules["max_games_total"]:
            over_scheduled = True
    return all_satisfied or over_scheduled


def get_play_count(potential_game):
    sum_history = 0
    for player in potential_game:
        for p in potential_game:
            sum_history += player.game_count
    return sum_history


def create_failure_scenarios():
    failing_scenarios = {}
    failing_scenarios["available slots"] = 0
    failing_scenarios["game length"] = 0
    failing_scenarios["players already scheduled"] = 0
    failing_scenarios["day or week failure"] = 0
    failing_scenarios["all players satisfied"] = 0
    return failing_scenarios


class SingleFlightScheduleTool:
    def __init__(self, flight_id, rules, players, gameslots):
        self.flight_id = flight_id
        self.rules = rules

        shuffle(gameslots)
        self.gameslots = sorted(gameslots, key=lambda gs: gs.facility_id, reverse=True)
        self.players = sorted(players, key=lambda player: player.availability_score)

    def check_escape_conditions(self, log=False):
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
        print("Generate Time Slot Player Pool")
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
        print("Run CA")
        tpp, ts = self.generate_timeslot_player_pool()
        ts_list = list(ts)
        shuffle(ts_list)
        all_scheduled_games = []
        init_histories(self.players)
        total_games_added = 0
        loop_count = 0
        games_considered = 0
        print("Start Loop")
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
        result = {}
        result["all_players_satisfied"] = self.all_players_satisfied()
        result["player_days_satisfied"] = self.player_days_satisfied()
        result["player_weeks_satisfied"] = self.player_weeks_satisfied()
        result["no_players_overscheduled"] = self.no_players_overscheduled()
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
                print(p.id)
            print()

    def recalculate_players(self):
        print("Recalculate Players")
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
        full_slots = [slot for slot in self.gameslots if slot.full == True]
        days = {}
        for slot in full_slots:
            if slot.day_number in days:
                days[slot.day_number].append(slot)
            else:
                days[slot.day_number] = [slot]
        return days

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

    def return_events(self):
        events = []
        for gameslot in self.gameslots:
            if gameslot.full is True:
                events.append(
                    {
                        'timeslot': gameslot.timeslot_id,
                        'facility': gameslot.facility_id,
                        'captain': gameslot.game_event[0].id,
                        'players': [p.id for p in gameslot.game_event],
                    }
                )
        return events

    def all_players_satisfied(self):
        for player in self.players:
            if player.satisfied == False:
                return False
        return True

    def no_players_overscheduled(self):
        for player in self.players:
            if player.game_count > player.rules["max_games_total"]:
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
                if days[key] > player.rules["max_games_day"]:
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
                if weeks[key] > player.rules["max_games_week"]:
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
                if days[key] > player.rules["max_games_day"]:
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
            print(i.id)
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
        return sum(
            [abs(p.rules["min_games_total"] - p.game_count) for p in self.players]
        ) / len(self.players)

    def average_player_satisfaction(self):
        return len([p for p in self.players if p.satisfied is False]) / len(
            self.players
        )

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
                print(p.id, p.game_count)
