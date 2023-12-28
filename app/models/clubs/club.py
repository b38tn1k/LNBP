from app.models import db, Model
from app.models import ModelProxy, transaction


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
    todos = db.relationship('Todo', back_populates='club', lazy='dynamic')

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
        db.session.add(club)
        db.session.commit()
        return club

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
        print(user.club.facilities)
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
            print('commit')

        return new_league

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
            (p for p in self.players 
             if set(p.first_name.split()).intersection(name_parts) 
             and set(p.last_name.split()).intersection(name_parts)),
            None
        )

        if player is None:
            
            # If no player found, create a new one with the first part as first name and the rest as last name
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else 'Unknown'
            player = self.new_player(first_name, last_name, add=add, commit=commit)
        return player
    
    def new_player(self, first_name, last_name, add=True, commit=False):
        player = ModelProxy.clubs.Player(
                first_name=first_name,
                last_name=last_name,
                email='placeholder@example.com',
                contact_number='000-000-0000',
                communication_preference_mobile=False,
                communication_preference_email=True,
                gender='Unknown',
                club_ranking=0,
                club=self
            )
        if add is True:
            db.session.add(player)

        if commit is True:
            db.session.commit()
        return player

    
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
