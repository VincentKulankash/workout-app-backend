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
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

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
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    workout_exercises = db.relationship('WorkoutExercise', back_populates = 'workout', cascade='all, delete-orphan')

    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name  = 'duration_must_be_positive'),
    )

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError('Duration must be a positive integer')
        return duration
     
    def __repr__(self):
        return f"<Workout {self.id}: {self.date}>"

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    reps = db.Column(db.Integer, nullable = False)
    sets = db.Column(db.Integer, nullable = False)
    duration_seconds = db.Column(db.Integer)
    workout = db.relationship('Workout', back_populates = 'workout_exercises') 
    exercise = db.relationship('Exercise', back_populates ='workout_exercises')

    __table_args__ = (
        UniqueConstraint('workout_id', 'exercise_id', name = 'unique_workout_exercise'),
        CheckConstraint('reps >= 0', name = 'reps_must_be_non_negative'),
        CheckConstraint('sets >= 0', name = 'sets_must_be_non_negative'),
    )

    @validates('reps', 'sets', 'duration_seconds')
    def validates_metrics(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} cannot be negative.")
        return value

    def __repr__(self):
        return f"<WorkoutExercise Workout:{self.workout_id} Exercise:{self.exercise_id}>"