from .player import *
from .gameslots import *
from .utils import *
from random import shuffle

class CaptainAssigner():
    def __init__(self, flight):
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
        count = 0
        for p in self.players:
            count += (p.captain_count >= p.rules["minCaptained"])
        return count == len(self.players)
    
    def all_games_captained(self):
        for g in self.gameslots:
            if g.full is True and g.captain is None:
                return False
        return True
    
    def reset_captaining(self):
        for p in self.players:
            p.captain_count = 0
        for g in self.gameslots:
            g.captain = None
    
    def assign_captains(self):
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
