from app.models import db, Model

class LeagueRules(Model):
    __tablename__ = 'league_rules'

    id = db.Column(db.Integer, primary_key=True)
    assume_busy = db.Column(db.Boolean, default=False)
    min_games_total = db.Column(db.Integer, default=4)
    max_games_total = db.Column(db.Integer, default=4)
    min_games_day = db.Column(db.Integer, default=0)
    max_games_day = db.Column(db.Integer, default=1)
    min_games_week = db.Column(db.Integer, default=0)
    max_double_headers = db.Column(db.Integer, default=0)
    max_concurrent_games = db.Column(db.Integer, default=2)
    max_games_week = db.Column(db.Integer, default=1)
    min_captained = db.Column(db.Integer, default=1)
    max_captained = db.Column(db.Integer, default=-1)
    max_week_gap = db.Column(db.Integer, default=2)
    players_per_match = db.Column(db.Integer, default=4)
    minimum_subs_per_game = db.Column(db.Float, default=0.7)

    league_id = db.Column(db.Integer, db.ForeignKey('league.id'), nullable=False)
    league = db.relationship('League', backref=db.backref('rules', uselist=False, cascade='all, delete-orphan'))

    GDPR_EXPORT_COLUMNS = {}
