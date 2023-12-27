from app.models import db, Model
from datetime import timedelta

class Timeslot(Model):
    __tablename__ = 'timeslot'

    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    # Foreign Key for League
    league_id = db.Column(db.Integer, db.ForeignKey('league.id', ondelete='CASCADE'))

    # Relationship to League
    league = db.relationship('League', backref=db.backref('timeslots', lazy=True, cascade='all, delete-orphan'))

    GDPR_EXPORT_COLUMNS = {}

    def __repr__(self):
        return f'<Timeslot - {self.human_readable_hhmm_dayname_mdy()}>'

    def human_readable_hhmm_mdy(self):
        return self.start_time.strftime('%H:%M %m/%d/%Y')

    def human_readable_hhmm_dayname_mdy(self):
        return self.start_time.strftime('%H:%M %A %m/%d/%Y')

    def human_readable_hhmm(self):
        return self.start_time.strftime('%H:%M')

    def human_readable_dayname_monthname(self):
        return self.start_time.strftime('%A %B')

    def human_readable_hhmm_mmdd(self):
        return self.start_time.strftime('%H:%M %m/%d')
    
    def human_readable_mmdd_hhmm(self):
        return self.start_time.strftime('%m/%d %H:%M')
    
    def get_duration(self):
        duration = self.end_time - self.start_time
        return int(duration.total_seconds() / 60)
