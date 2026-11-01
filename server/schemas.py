from marshmallow import validate, ValidationError, fields, Schema, validates_schema


#schema validations 
#Name must be at least 2 characters
#Category must be one of the specified strings
#Duration/reps/sets must be positive integers

class ExerciseSchema(Schema):
    id = fields.Int(dump_only= True) #Dump only menas client cant send an id only receive it
    name = fields.Str(required= True, validate=validate.Length(min=2, error='Name must be at least 2 characters.'))
    category = fields.Str(required= True, validate=validate.OneOf(
        ['strength', 'cardio', 'flexibility', 'balance'],
        error='Category must be one of strength, cardio, flexibility or balance'
    ))
    equipment_needed = fields.Bool(load_default=False)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, error='Duration must be greater than  0.'))
    notes = fields.Str(allow_none=True)

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(required=True, validate=validate.Range(min=0))
    sets = fields.Int(required=True, validate=validate.Range(min=0))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=0))

    @validates_schema
    def validate_metrics(self, data, **kwargs):
        if not data.get('reps') and not data.get('sets') and not data.get('duration_seconds'):
            raise ValueError("You must provide at least one of: reps, sets or duration_seconds.")

class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Method('get_nested_exercises')

    def get_nested_exercises(self, workout):
        return [
            {
                'id': we.id,
                'exercise_id': we.exercise_id,
                'exercise_name': we.exercise.name,
                'reps': we.reps,
                'sets': we.sets,
                'duration_seconds': we.duration_seconds
            } for we in workout.workout_exercises
        ]

class ExerciseDetailSchema(ExerciseSchema):
    workouts = fields.Method('get_nested_workouts')

    def get_nested_workouts(self, exercise):
        return [
            {
                "id": we.workout.id,
                "date": str(we.workout.date),
                "duration_minutes": we.workout.duration_minutes,
                "reps": we.reps,
                "sets": we.sets
            } for we in exercise.workout_exercises
        ]
