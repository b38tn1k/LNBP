from app.models import db, Model
from app.models import ModelProxy, transaction
from sqlalchemy.orm.attributes import flag_modified
from flask import url_for


class Club(Model):
    __tablename__ = "club"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    contact_number = db.Column(
        db.String(50)
    )  # Assuming phone number format suits a max length of 50
    street_address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))  # Assuming state name or abbreviation
    zip_code = db.Column(
        db.String(15)
    )  # Adjust length based on the country's ZIP/Postal code format
    country = db.Column(db.String(100))
    todos = db.relationship("Todo", back_populates="club", lazy="dynamic")
    bg_statistics = db.Column(db.JSON)
    country = db.Column(db.String(100))
    portal_style = db.Column(db.String(100), default='lux.min.css')

    GDPR_EXPORT_COLUMNS = {
        "id": "ID of the club",
        "email": "Club Email",
        "contact_number": "Club Contact Number",
        "street_address": "Club Street Address",
        "city": "Club City",
        "state": "Club state / region / province",
        "zip_code": "Club postal code",
        "country": "Club country",
    }

    @staticmethod
    def create(name):
        """
        This function creates a new instance of the `Club` class and adds it to
        the database.

        Args:
            name (str): The `name` input parameter is passed as a string value to
                the constructor of the `Club` class and sets the `name` attribute
                of the instance being created.

        Returns:
            : The output returned by this function is a `Club` object named after
            the `name` argument passed to the function.

        """
        club = Club(name=name)
        club.bg_statistics = {}
        db.session.add(club)
        db.session.commit()
        return club
    
    def get_portal_style(self):
        if self.portal_style is None:
            # self.portal_style = 'lux.min.css'
            self.portal_style = 'superhero.min.css'
        return url_for('static', filename='css/portal_styles/' + self.portal_style)


    def update_statistics(self, item):
        """
        This function updates the "background statistics" of an object (hence the
        name "update_statistics") and prints out the current statistics. It takes
        an item as an argument and adds one to the count of that item if it's
        already present; otherwise ,it initializes the count for that item to one.
        Finally; this function modifies the object's flags to indicate modifications
        to the "bg_statistics" attribute.. The printing part then iterates through
        the background statistics and prints out each key(an item) along with its
        respective count (background statistics).

        Args:
            item (str): The `item` input parameter is used to update the statistics
                of a specific item.

        """
        if item in self.bg_statistics:
            self.bg_statistics[item] += 1
        else:
            self.bg_statistics[item] = 1
        flag_modified(self, "bg_statistics")

        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        MAGENTA = "\033[95m"
        CYAN = "\033[96m"
        WHITE = "\033[97m"
        RESET = "\033[0m"

        print(RED, "Algorithm Stats", RESET)
        for key in self.bg_statistics:
            print("  ", MAGENTA, key, RESET , self.bg_statistics[key])
        print("Most Recent Success: ", item)

    # Relationships and other methods as required
    @transaction
    def add_facility(self, name, asset_type, user, club):
        """
        This function creates a new Facility object and assigns it to a user's club.

        Args:
            name (str): The `name` input parameter is used to set the name of the
                newly created facility.
            asset_type (str): The `asset_type` input parameter indicates the type
                of asset being added (e.g.
            user (): The `user` input parameter is used to set the owner of the
                newly created facility.
            club (): The `club` input parameter passes the club object to which
                the new facility will be added.

        Returns:
            : The function `add_facility` returns the newly created `Facility`
            object named `facility`.

        """
        facility = ModelProxy.clubs.Facility.create(name, asset_type, club)
        facility_admin = ModelProxy.clubs.FacilityAdministrator(
            user=user, facility=facility
        )
        return facility

    @transaction
    def create_league(
        self, name, league_type, start_date, end_date, add=True, commit=False
    ):
        """
        Create a new league associated with this club.

        :param name: Name of the league.
        :param league_type: Type of the league.
        :param start_date: Start date of the league.
        :param bg_color: Background color of the league.
        :param fg_color: Foreground color of the league.
        :return: Created League instance.
        """
        # Create a new League instance
        new_league = ModelProxy.clubs.League(
            name=name,
            type=league_type,
            start_date=start_date,
            end_date=end_date,
            club=self,
        )

        if add is True:
            db.session.add(new_league)
        if commit is True:
            db.session.commit()
            print("commit")

        return new_league

    def get_facility_by_id(self, id):
        """
        This function retrieves the facility with the given ID from a list of
        facilities by iterating over the list and returning the first facility
        that matches the ID or `None` if no match is found.

        Args:
            id (int): The `id` input parameter is used to filter the list of
                facilities and retrieve a specific facility by its ID.

        Returns:
            : The function returns `None`.

        """
        return next((f for f in self.facilities if f.id == id), None)

    def get_league_by_id(self, league_id):
        """
        Get a league by its ID, ensuring it belongs to this club.

        :param league_id: The ID of the league to retrieve.
        :return: The League instance if found, otherwise None.
        """
        # Use the relationship 'leagues' to filter by league ID
        return next((league for league in self.leagues if league.id == league_id), None)

    def find_or_create_player(self, full_name, add=True, commit=False):
        """
        Check if a player with a similar name is in the club, and return them if so.
        If not, create a new temporary player with the name and return the new model.

        :param full_name: The full name of the player.
        :return: Player instance.
        """
        # Normalize the full_name by splitting and removing extra spaces
        name_parts = full_name.split()

        # Search for a player with a matching part in their first and last name in the club
        player = next(
            (
                p
                for p in self.players
                if set(p.first_name.split()).intersection(name_parts)
                and set(p.last_name.split()).intersection(name_parts)
            ),
            None,
        )

        if player is None:
            # If no player found, create a new one with the first part as first name and the rest as last name
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else "Unknown"
            player = self.new_player(first_name, last_name, add=add, commit=commit)
        return player

    def new_player(self, first_name, last_name, add=True, commit=False):
        """
        This function creates a new instance of the `Player` model and optionally
        adds it to the database.

        Args:
            first_name (str): The `first_name` input parameter sets the value of
                the `first_name` attribute of the new player object.
            last_name (str): The `last_name` input parameter creates a new instance
                of the `Player` class with the given first name and last name for
                the Player object being created.
            add (bool): The `add` input parameter to the `new_player` function
                determines whether or not to add the newly created `Player` object
                to the database immediately.
            commit (bool): The `commit` input parameter determines whether to
                commit the changes made to the database after creating a new
                `Player` object.

        Returns:
            : The output returned by this function is a `ModelProxy` object of
            type `clubs.Player`.

        """
        player = ModelProxy.clubs.Player(
            first_name=first_name,
            last_name=last_name,
            email="placeholder@example.com",
            contact_number="000-000-0000",
            communication_preference_mobile=False,
            communication_preference_email=True,
            gender="Unknown",
            club_ranking=0,
            club=self,
        )
        if add is True:
            db.session.add(player)

        if commit is True:
            db.session.commit()
        return player

    def get_player_by_id(self, id):
        """
        The given function `get_player_by_id` takes an integer `id` as input and
        returns the player object associated with that ID or `None` if no player
        found.

        Args:
            id (int): The `id` input parameter is used to search for a player with
                the matching ID within the `players` list.

        Returns:
            None: The output returned by this function is `None`.

        """
        for p in self.players:
            if p.id == id:
                return p
        return None

    def add_todo(self, task, add=True, commit=False):
        """
        Create and add a new todo item to this club.

        Args:
            task (str): The task or description of the todo item.

        Returns:
            Todo: The newly created Todo instance.

        Usage:
            club = Club.query.get(club_id)
            todo = club.add_todo('Prepare annual budget report')
        """
        todo = ModelProxy.clubs.Todo(task=task, club_id=self.id)

        if add is True:
            db.session.add(todo)

        if commit is True:
            db.session.commit()

        return todo

    def __repr__(self):
        """
        This function defines the `__repr__` method for the `Club` object.

        Returns:
            str: The output returned by the `__repr__()` function would be:

            "`<Club 0 - name>`"

        """
        return "<Club {0} - {1}>".format(self.id, self.name)
