from app import db
from .player import Player
from .court import Court
from .league import League
from . import Model


class Club(Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def empty(self):
        # Delete all players associated with this club
        for player in self.players:
            db.session.delete(player)

        # Delete all courts associated with this club
        for court in self.courts:
            db.session.delete(court)

        for league in self.leagues:
            league.delete(False)
            db.session.delete(league)
        
        db.session.commit()

    def delete_all_associated_records(self):
        for u in self.users:
            db.session.delete(u)
        # Delete all players associated with this club
        for player in self.players:
            db.session.delete(player)

        # Delete all courts associated with this club
        for court in self.courts:
            db.session.delete(court)

        for league in self.leagues:
            league.delete(False)
            db.session.delete(league)

        db.session.commit()


    def __repr__(self):
        return '<Club {}>'.format(self.name)
    
    def add_player(self, player_name, player_email):
        check = Player.query.filter_by(player_email=player_email, club=self).first()
        if (check is None):
            player = Player(player_name=player_name, player_email=player_email, club_id=self.id, club=self)
            db.session.add(player)
            db.session.commit()
            return player
        return check

    def add_court(self, court_name, commit=True):
        check = Court.query.filter_by(court_name=court_name, club=self).first()
        if check is None:
            court = Court(court_name=court_name, club=self)
            db.session.add(court)
            if commit:
                db.session.commit()
            return court
        return check
    
    def add_league(self, league_name, commit=True):
        check = League.query.filter_by(league_name=league_name, club=self).first()
        if check is None:
            league = League(league_name=league_name, club=self)
            db.session.add(league)
            if commit:
                db.session.commit()
            return league
        return None
    
    def get_league(self, league_id):
        league = [league for league in self.leagues if league.id == league_id][0]
        return league
    
    def has_user(self, user):
        return user in self.users
    
    def has_court(self, court):
        return court.club_id == self.id
    
    def get_court_by_name(self, name):
        for c in self.courts:
            if c.court_name == name:
                return c
        return None

