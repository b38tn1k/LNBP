from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from . import Model


@login.user_loader
def load_user(id):
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
        if (self.club_authenticated is None or self.club_authenticated == 0):
            self.club_authenticated = 1
        else:
            self.club_authenticated = 0

    # def get_topscore(self):
    #     return self.topscore
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_email(self, email):
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_club(self, club):
        self.club = club

    def __repr__(self):
        return '<User {}>'.format(self.username)

