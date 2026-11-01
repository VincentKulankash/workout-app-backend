from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from .models import db, Workout, Exercise, WorkoutExercise
from .schemas import (
    ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema,
    WorkoutDetailSchema, ExerciseDetailSchema
)

#create a blueprint
#this acts like a mini flask app it holds the routes so i can import them to app.py
#it helps avoid circular import errors 
routes_bp = Blueprint('routes', __name__)

# Initialize schemas
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()
exercise_detail_schema = ExerciseDetailSchema()
workout_exercise_schema = WorkoutExerciseSchema()

#Workout routes

#GET all workouts
@routes_bp.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    # Use schema to serialize (dump) the list of workouts
    return jsonify(workouts_schema.dump(workouts)), 200

#GET a single workout
@routes_bp.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    # Use detail schema to include nested exercises (Stretch Goal!)
    return jsonify(workout_detail_schema.dump(workout)), 200

#POST workouts
@routes_bp.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    try:
        # Load and validate data using Schema
        validated_data = workout_schema.load(data)
        
        new_workout = Workout(**validated_data)
        db.session.add(new_workout)
        db.session.commit()
        
        return jsonify(workout_schema.dump(new_workout)), 201
    except ValidationError as err:
        # Return schema validation errors as JSON!
        return jsonify({"errors": err.messages}), 400

#DELETE workouts
@routes_bp.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit() #Cascade delete in models.py ensures WorkoutExercises are also removed
    return jsonify({"message": "Workout deleted"}), 200


#Exercise Routes 
#GET all Exercises
@routes_bp.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200

#GET a single exercise
@routes_bp.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    # Use detail schema to include nested workouts
    return jsonify(exercise_detail_schema.dump(exercise)), 200

#POST an exercise 
@routes_bp.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        validated_data = exercise_schema.load(data)
        new_exercise = Exercise(**validated_data)
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(new_exercise)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

#DELETE an exercise
@routes_bp.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'Exercise deleted'}), 200


#JOIN table routes 
#POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
@routes_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    Workout.query.get_or_404(workout_id)
    Exercise.query.get_or_404(exercise_id)

    data = request.get_json()
    # Inject the IDs from the URL into the data before validating
    data['workout_id'] = workout_id
    data['exercise_id'] = exercise_id
    
    try:
        validated_data = workout_exercise_schema.load(data)
        new_we = WorkoutExercise(**validated_data)
        db.session.add(new_we)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(new_we)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400