from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from . import Model


@login.user_loader
def load_user(id):
    """
    This function `load_user` takes an ID as an input and returns a user object
    from the database using SQLAlchemy's query API.

    Args:
        id (int): In the given function `load_user(id)`, the `id` input parameter
            is used as a key to retrieve a specific User object from the database
            using SQLAlchemy's query method.

    Returns:
        : The output of the function `load_user(id)` will be `None` if there is
        no user with the provided `id`.

    """
    return User.query.get(int(id))


class User(UserMixin, Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    club_authenticated = db.Column(db.Integer, default=0)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id', name='user_admined_club'))
    club = db.relationship('Club', backref='users')

    def toggle_auth(self):
        """
        This function toggles the value of `self.club_authenticated` between 0 and
        1.

        """
        if (self.club_authenticated is None or self.club_authenticated == 0):
            self.club_authenticated = 1
        else:
            self.club_authenticated = 0

    # def get_topscore(self):
    #     return self.topscore
    
    def set_password(self, password):
        """
        This function sets the `password_hash` attribute of the object to a hash
        value generated from the passed `password` using the `generate_password_hash()`
        function.

        Args:
            password (str): The `password` input parameter sets the value of the
                instance's `password_hash`.

        """
        self.password_hash = generate_password_hash(password)

    def set_email(self, email):
        """
        The given function `set_email` takes an email address as input and assigns
        it to the object's `email` attribute.

        Args:
            email (str): The `email` input parameter sets the value of the instance
                variable `self.email` within the function.

        """
        self.email = email

    def check_password(self, password):
        """
        This function checks if a given password "password" matches the stored
        password hash "self.password_hash".

        Args:
            password (str): The `password` input parameter is used to compare the
                provided password against the stored hashed password for authentication
                purposes.

        Returns:
            bool: The function `check_password()` takes no arguments and returns
            `None`, as stated explicitly with the `return None` statement at the
            end of the function body.

        """
        return check_password_hash(self.password_hash, password)
    
    def set_club(self, club):
        """
        This function sets the `club` attribute of the object to the specified
        `club` argument.

        Args:
            club (str): The `club` input parameter is assigned to the `self.club`
                attribute of the class.

        """
        self.club = club

    def __repr__(self):
        """
        This function defines a `__repr__()` method for a custom object that
        displays the user's username when the object is represented as a string.

        Returns:
            str: The output returned by the `__repr__` function is `<User {}>`.

        """
        return '<User {}>'.format(self.username)

