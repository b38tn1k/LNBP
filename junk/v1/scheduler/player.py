from .utils import *
import copy


class Player:
    def __init__(self, player_obj, flight_id, availability_template, rules):
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
                if self.days.count(g.day_number) < self.rules["maxGamesDay"] and self.days.count(g.day_number) < self.rules["maxGamesDay"]:
                    potentials.append(g)
        self.potentials = potentials
        return potentials

    def add_game_event(self, gameslot):
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
        res = self.availability[gameslot.timeslot_id]
        return res == AVAILABLE or res == AVAILABLE_LP