from datetime import date
from . import db

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.Date, nullable=False, default=date.today)

class HabitCheckin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    day = db.Column(db.Date, nullable=False, index=True)

    habit = db.relationship('Habit', backref=db.backref('checkins', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('habit_id', 'day', name='uq_habit_day'),
    )
