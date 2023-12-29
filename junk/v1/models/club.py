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
        """
        This function empties an object of all its associated players and courts
        and delete those objects as well.

        """
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
        """
        This function deletes all associated records of a Club instance from the
        database.

        """
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
        """
        This function defines a special method (specifically the `__repr__` method)
        for the class `Club`.

        Returns:
            str: The output returned by this function is "<Club>".

        """
        return '<Club {}>'.format(self.name)
    
    def add_player(self, player_name, player_email):
        """
        This function adds a new player to the club database table if the email
        address is not already taken by another player of the same club.

        Args:
            player_name (str): The `player_name` input parameter is used to set
                the `Player.player_name` attribute for the new player object that
                will be created if a player with the given email does not already
                exist.
            player_email (str): In this function `player_email` is used as a lookup
                value to check if there is already a player with the same email
                address currently associated with the club.

        Returns:
            : The output returned by this function is `check`, which is `None` if
            there is no existing player with the same email address as the input
            `player_email`, or the existing player object if one exists.

        """
        check = Player.query.filter_by(player_email=player_email, club=self).first()
        if (check is None):
            player = Player(player_name=player_name, player_email=player_email, club_id=self.id, club=self)
            db.session.add(player)
            db.session.commit()
            return player
        return check

    def add_court(self, court_name, commit=True):
        """
        This function adds a new Court object to the database and returns it if
        one was found or adds it if one was not found.

        Args:
            court_name (str): The `court_name` input parameter is used to identify
                the specific court that should be added or retrieved.
            commit (bool): The `commit` parameter is a boolean value that determines
                whether to commit the changes made to the database after adding a
                new `Court` object.

        Returns:
            : The output of this function is either the new `Court` object if one
            was added (in which case `commit` is True), or the existing `Court`
            object found by the query if one already existed (in which case `commit`
            is False).

        """
        check = Court.query.filter_by(court_name=court_name, club=self).first()
        if check is None:
            court = Court(court_name=court_name, club=self)
            db.session.add(court)
            if commit:
                db.session.commit()
            return court
        return check
    
    def add_league(self, league_name, commit=True):
        """
        This function adds a new league with the given name to the club associated
        with the object that calls it.

        Args:
            league_name (str): The `league_name` input parameter specifies the
                name of the league that the function is being called to add to the
                club.
            commit (bool): The `commit` input parameter controls whether the changes
                made to the database by this function should be committed immediately
                after they are made. If `commit=True`, the changes will be committed
                and written to the database.

        Returns:
            None: Based on the code provided:
            
            The output returned by this function is "None" if a league with the
            same name already exists for the club passed as an argument.

        """
        check = League.query.filter_by(league_name=league_name, club=self).first()
        if check is None:
            league = League(league_name=league_name, club=self)
            db.session.add(league)
            if commit:
                db.session.commit()
            return league
        return None
    
    def get_league(self, league_id):
        """
        This function retrieves the league with the given ID from a list of leagues
        stored internally and returns the found league as a single entity.

        Args:
            league_id (int): The `league_id` input parameter specifies the ID of
                the league to be retrieved from the list of leagues stored by the
                `self.leagues` attribute.

        Returns:
            list: The output returned by this function is a single league object
            with the ID matching the one provided as an argument.

        """
        league = [league for league in self.leagues if league.id == league_id][0]
        return league
    
    def has_user(self, user):
        """
        This function checks if a given `user` is present In the list of users
        stored In the object.

        Args:
            user (list): The `user` input parameter is passed as an argument to
                the `has_user()` function and is used to look up the existence of
                the given user within the list of users stored within the object.

        Returns:
            bool: The output returned by this function is `False`.

        """
        return user in self.users
    
    def has_court(self, court):
        """
        This function `has_court()` checks if the given `court` object has the
        same `club_id` as the object that is calling the function.

        Args:
            court (): The `court` input parameter is used to check if the court
                belongs to the same club as the object itself.

        Returns:
            bool: The output returned by this function is `True` if the given
            `court` has the same `club_id` as the object on which the method is
            called (i.e., if the court is associated with the same club as the
            object), and `False` otherwise.

        """
        return court.club_id == self.id
    
    def get_court_by_name(self, name):
        """
        This function takes a string `name` as input and returns the court object
        with that name from a list of courts or returns `None` if no such court exists.

        Args:
            name (str): The `name` input parameter is a string that is used to
                search for a court with a matching name among the list of courts
                stored within the object.

        Returns:
            None: The function `get_court_by_name()` returns `None` because no
            court with the given name exists within the list of `self.courts`.

        """
        for c in self.courts:
            if c.court_name == name:
                return c
        return None

