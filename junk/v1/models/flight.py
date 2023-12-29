from .timeslot import Timeslot
from . import flight_player_association, Model
from app import db
import json


class Flight(Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_name = db.Column(db.String(64), index=True)
    league_id = db.Column(db.Integer, db.ForeignKey('league.id', name='admined_league'))
    league = db.relationship('League', backref='flights')
    timeslots = db.relationship('Timeslot', backref='flight', lazy='dynamic')
    bg_color = db.Column(db.String(7), default='#000000')
    fg_color = db.Column(db.String(7), default='#ffffff')
    players = db.relationship(
        'Player',
        secondary=flight_player_association,
        lazy='dynamic'
    )

    def print_timeslots_and_events(self):
        total_timeslots = self.timeslots.count()
        print(f"Total timeslots in {self.flight_name}: {total_timeslots}")

        for timeslot in self.timeslots:
            num_events = len(timeslot.events)
            print(f"Timeslot {timeslot.id} (from {timeslot.start_time} to {timeslot.end_time}): {num_events} events")

    def on_delete(self):
        self.clean_players(False)
        self.delete_timeslots(False)

    def get_other_court_events(self):
        collisions = []
        for timeslot in self.timeslots:
            for court in timeslot.courts:
                res = court.get_colliding_events(timeslot, self.id)
                for r in res:
                    collisions.append(r)
        return collisions

    def get_all_courts(self):
        """
        Get a sorted list of all courts used in the flight's timeslots.
        """
        all_courts = set()  # Use a set to collect unique courts
        for timeslot in self.timeslots:
            all_courts.update(timeslot.courts)  # Use 'update' to add elements to the set
        return sorted(all_courts, key=lambda court: court.court_name)

    def get_flight_dimensions(self):
        y = len(self.timeslots)
        x = 0
        for timeslot in self.timeslots.all():
            if len(timeslot.courts > x):
                x = len(timeslot.courts)
        return [x, y]

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)
            db.session.commit()

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
            db.session.commit()

    def player_in_flight(self, player):
        return player in self.players

    def generate_schedule_CSV(self):
        csv_list = []

        header1 = []
        header1.append(self.flight_name)
        for timeslot in self.get_sort_timeslots():
            header1.append(timeslot.get_human_readable_date_day_month())
        csv_list.append(header1)

        header2 = [" "]
        for timeslot in self.get_sort_timeslots():
            header2.append(timeslot.get_human_readable_time())
        csv_list.append(header2)

        for player in self.players:
            player_row = [player.player_name]
            for timeslot in self.get_sort_timeslots():
                game = ''
                events = timeslot.get_events()
                for e in events:
                    # print(e)
                    if e['captain'] == player.id:
                        game += "C"
                    if player.id in e['players']:
                        game += e['court_name']
                player_row.append(game)
            csv_list.append(player_row)

        rows = []
        for row in csv_list:
            rows.append(', '.join(row))
        csv = '\n'.join(rows)
        return csv
    
    def get_player_availability(self):
        a = {}
        for player in self.players:
            avail = player.get_availability_obj_for_flight(self.id)
            a[player.id] = avail
        return a
    
    def get_events(self):
        a = []
        for timeslot in self.timeslots.all():
            es = timeslot.get_events()
            for e in es:
                a.append(e)
        return a

    def get_event_objects(self):
        a = []
        for timeslot in self.timeslots.all():
            es = timeslot.get_event_objects()
            for e in es:
                a.append(e)
        return a

    def __repr__(self):
        return '<Flight {}>'.format(self.flight_name)
    
    def delete_timeslots(self, commit=True):
        for timeslot in self.timeslots.all():
            timeslot.on_delete()
            db.session.delete(timeslot)
        if commit:
            db.session.commit()

    def delete_events(self):
        for timeslot in self.timeslots.all():
            timeslot.delete_all_events(False)
        db.session.commit()
    
    def create_timeslot(self, start_time, end_time, courts):
        # Search for a timeslot in flight.timeslots with matching start and end times
        matching_timeslot = next((ts for ts in self.timeslots if ts.start_time == start_time and ts.end_time == end_time), None)

        if matching_timeslot is None:
            timeslot = Timeslot(start_time=start_time, end_time=end_time, flight=self)
            for court in courts:
                timeslot.courts.append(court)
            db.session.add(timeslot)
            db.session.commit()
            return timeslot.id

        return matching_timeslot.id

    def get_sort_timeslots(self):
        return sorted(self.timeslots, key=lambda x: x.start_time.isoformat()[5:10])
    
    def clean_players(self, commit=True):
        for player in self.players:
            player.remove_availability_for_flight(self.id)
        if commit:
            db.session.commit()

    def get_timeslots_json(self):
        timeslots_list = []
        for timeslot in self.get_sort_timeslots():
            court_ids = [court.id for court in timeslot.courts.all()]
            # TODO need to check if court is already busy!
            timeslot_dict = {
                'id': timeslot.id,
                'title': timeslot.flight.flight_name,
                'start': timeslot.start_time.isoformat(),
                'end': timeslot.end_time.isoformat(),
                'display': 'block',
                'backgroundColor': self.bg_color,
                'textColor': self.fg_color,
                'courts': court_ids,
            }
            timeslots_list.append(timeslot_dict)
        return json.dumps(timeslots_list)
    
    # method to get timeslot by id
    def get_timeslot_by_id(self, timeslot_id):
        return self.timeslots.filter_by(id=timeslot_id).first()

    # method to get player by id
    def get_players_by_id(self, player_id):
        return self.players.filter_by(id=player_id).first()

