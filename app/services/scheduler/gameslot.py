import statistics
from random import choice
from .constants import *

class GameSlot:
    def __init__(self, tid, fid, y2k_counter, rules):
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

    def __hash__(self):
        return self.timeslot_id + self.facility_id

    def duplicate(self):
        return type(self)(self.timeslot_id, {'days': self.day_number, 'weeks': self.week_number}, self.rules)

    def copy_with_events(self):
        gs = self.duplicate()
        for p in self.game_event:
            gs.game_event.append(p)
        gs.full = self.full
        return gs

    def log(self, dofilter=True):
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
        isNew = not (player in self.game_event)
        isAvailable = (player.availability[self.timeslot_id] == AVAILABLE) or (
            player.availability[self.timeslot_id] == AVAILABLE_LP
        )
        dayCountOk = player.days.count(self.day_number) < player.rules["maxGamesDay"]
        weekCountOk = player.days.count(self.day_number) < player.rules["maxGamesWeek"]
        return isNew and isAvailable and dayCountOk and weekCountOk

    def __eq__(self, other):
        if isinstance(other, GameSlot):
            c1 = self.timeslot_id = other.timeslot_id
            c2 = self.timeslot_id = other.timeslot_id
            return c1 and c2
        return False

    def add_player_to_match(self, player):
        if self.player_can_be_added(player):
            player.add_game_event(self)
            self.game_event.append(player)
            if len(self.game_event) == self.rules["playersPerMatch"]:
                self.full = True
            self.captain = choice(self.game_event)

    def force_player_to_match(self, player):
        print("Force Player To Match")
        player.add_game_event(self)
        self.game_event.append(player)
        if len(self.game_event) == self.rules["players_per_match"]:
            self.full = True

    def get_most_available_player(self):
        lead = self.game_event[0]
        for player in self.game_event[1:]:
            if player.availability_score > lead.availability_score:
                lead = player
        return lead

    def get_most_served_player(self):
        lead = self.game_event[0]
        for player in self.game_event[1:]:
            if player.game_count > lead.game_count:
                lead = player
        return lead

    def get_swap_candidate_player(self):
        # Compute the median availability score
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
        tas = 0
        for player in self.game_event:
            tas += player.availability_score
        return tas

    def get_player_match_history_score(self):
        scores = []
        for player in self.game_event:
            scores.append(player.get_total_match_history_score(self))
        return scores

    def is_building_already(self):
        return len(self.game_event) > 0 and not (self.full)

    def remove_player_from_match(self, player):
        player.remove_game_event(self)
        if player in self.game_event:
            self.game_event.remove(player)
        self.full = False

    def all_players_satisfy_min_games(self):
        return all(
            player.game_count > player.rules["minGamesTotal"]
            for player in self.game_event
        )

    def destruct(self):
        for player in self.game_event:
            player.remove_game_event(self)
        self.game_event = []
        self.full = False

    def self_destruct_if_unneccessary(self):
        if self.all_players_satisfy_min_games():
            self.destruct()

    def self_destruct_if_incomplete(self):
        if not (self.full):
            self.destruct()

    def get_players_available_to_swap(self, other_match):
        available_players = []
        for player in self.game_event:
            if other_match.hypothetically_player_can_be_added(player):
                available_players.append(player)
        return available_players

    def logps(self, ps):
        for p in ps:
            print(p.player_name)

    def get_inverse_players(self, players):
        inverse = []
        for p in self.game_event:
            if not (p in players):
                inverse.append(p)
        return inverse

    def compare_histories_stay(self, group, stay, go):
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

    def try_exchange(self, other_match, try_hard=False):
        owned_players_can_go = self.get_players_available_to_swap(other_match)
        other_players_can_go = other_match.get_players_available_to_swap(self)
        if len(owned_players_can_go) > 0 and len(other_players_can_go) > 0:
            owned_players_must_stay = self.get_inverse_players(owned_players_can_go)
            other_players_must_stay = other_match.get_inverse_players(
                other_players_can_go
            )
            own_players_swap_scores = self.compare_histories_stay(
                owned_players_can_go, owned_players_must_stay, other_players_must_stay
            )
            other_players_swap_scores = other_match.compare_histories_stay(
                other_players_can_go, other_players_must_stay, owned_players_must_stay
            )
            best_own_player = max(
                own_players_swap_scores, key=lambda x: x["stay_score"]
            )["player"]
            best_other_player = min(
                other_players_swap_scores, key=lambda x: x["go_score"]
            )["player"]
            # double check
            new_possible_own = self.get_inverse_players([best_own_player])
            new_possible_other = other_match.get_inverse_players([best_other_player])
            good_for_own = (
                best_own_player.get_sum_history(new_possible_own)
                > best_own_player.get_sum_history(new_possible_other)
                or try_hard
            )
            good_for_other = (
                best_other_player.get_sum_history(new_possible_other)
                > best_other_player.get_sum_history(new_possible_own)
                or try_hard
            )
            if good_for_own and good_for_other:
                other_match.remove_player_from_match(best_other_player)
                self.remove_player_from_match(best_own_player)
                other_match.add_player_to_match(best_own_player)
                self.add_player_to_match(best_other_player)
                return True
        return False
        # check if players are available for the other match
        # check if other match players are available for this match
        # check if other match contains players in history greater than players in history in current match
        # do the same for this one
        # swap

    def get_sad_players_and_self(self):
        sad_players = []
        for player in self.game_event:
            if player.availability[self.timeslot_id] == AVAILABLE_LP:
                pg = {}
                pg["game"] = self
                pg["player"] = player
                sad_players.append(pg)
        return sad_players

    def calculate_history_delta(self, other_player, ignore_player):
        history_delta = 0
        for p in self.game_event:
            if p != ignore_player:
                history_delta += other_player.check_history_score(p)
        return history_delta
