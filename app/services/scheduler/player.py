import copy
from .constants import *


def min_games_total_exception(player):
    player.rules["min_games_total"] = 0


def maxDoubleHeadersDay_exception(player):
    player.rules["max_games_day"] = 2
    player.rules["max_games_week"] = 2


def maxDoubleHeadersWeek_exception(player):
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
        return self.id

    def set_availability_score_relation(self, mean_score):
        self.availability_score_greater_than_mean = self.availability_score > mean_score

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.id == other.id
        return False

    def find_potential_slots_in_current_layout(self, gameslots):
        potentials = []
        for g in gameslots:
            if self.availability[g.timeslot_id] == AVAILABLE or self.availability[g.timeslot_id] == AVAILABLE_LP:
                if self.days.count(g.day_number) < self.rules["max_games_day"] and self.days.count(g.day_number) < self.rules["max_games_day"]:
                    potentials.append(g)
        self.potentials = potentials
        return potentials

    def add_game_event(self, gameslot):
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
        if player.id in self.other_player_history:
            return self.other_player_history[player.id]
        else:
            return 0

    def get_most_history_player_in_match(self, match):
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
        if len(self.other_player_history):
            max_key = max(self.other_player_history, key=self.other_player_history.get)
            return {max_key: self.other_player_history[max_key]}
        else:
            return {0: 0}

    def get_total_match_history_score(self, match):
        res = 0
        for player in match.game_event:
            if player.id in self.other_player_history:
                res += self.other_player_history[player.id]
        return res

    def add_history(self, player):
        if player.id in self.other_player_history:
            self.other_player_history[player.id] += 1
            player.other_player_history[self.id] += 1
        else:
            self.other_player_history[player.id] = 1
            player.other_player_history[self.id] = 1

    def subtract_history(self, player):
        self.other_player_history[player.id] -= 1
        player.other_player_history[self.id] -= 1

    def get_history(self, player):
        if player.id in self.other_player_history:
            return self.other_player_history[player.id]
        else:
            return 0

    def get_sum_history(self, players):
        res = 0
        count = 0
        for p in players:
            count += 1
            res += self.get_history(p)
        if count == 0:
            count = 1
        return res / count

    def log(self, dofilter):
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
        res = self.availability[gameslot.timeslot_id]
        return res == AVAILABLE or res == AVAILABLE_LP
