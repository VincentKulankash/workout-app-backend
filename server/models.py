from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint

db = SQLAlchemy()

class Exercise(db.Model): 
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='unique_exercise_name'),
        CheckConstraint('length(name) > 0', name='name_cannot_be_empty'),
    )

    @validates('category')
    def validate_category(self, key, category):
        allowed = ['strength', 'cardio', 'flexibility', 'balance']

        if category.lower() not in allowed:
            raise ValueError (f"Category must be one of {allowed}")
        return category.lower()

    def __repr__(self):
        return f"<Exercise {self.id}: {self.name}>"

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        CheckConstraint('duration_minites > 0', name  = 'duration_must_bepositive'),
    )

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError('Duration must be a positive integer')
        return duration
     
    def __repr__(self):
        return f"<Workout {self.id}: {self.date}>"
