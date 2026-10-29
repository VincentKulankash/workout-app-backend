from flask import Blueprint, request, jsonify
from .models import db, Workout, Exercise, WorkoutExercise
from datetime import datetime

#create a blueprint
#this acts like a mini flask app it holds the routes so i can import them to app.py
#it helps avoid circular import errors 

routes_bp = Blueprint('routes', __name__)

#Workout routes

#GET all workouts
@routes_bp.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()

    return jsonify([{"id": w.id, "date": str(w.date), "duration_minutes": w.duration_minutes, "notes": w.notes} for w in workouts]), 200

#GET a single workout
@routes_bp.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return jsonify({
        'id': workout.id,
        'date': str(workout.date),
        'duration_minutes': workout.duration_minutes,
        'notes': workout.notes
    }), 200

#POST workouts
@routes_bp.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    try:
        workout_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        new_workout = Workout(
            date = workout_date,
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return jsonify({"id": new_workout.id, "message": "Workout created"}), 201
    except Exception as e:
        db.session.rollback() #undo the transaction if somethong fails

        return jsonify({"error": str(e)}), 400

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
    return  jsonify([{"id": e.id, "name": e.name, "category": e.category, "equipment_needed": e.equipment_needed,} for e in exercises]), 200

#GET a single exercise
@routes_bp.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return jsonify({
        'id': exercise.id,
        'name': exercise.name,
        'category': exercise.category,
        'equipment_needed': exercise.equipment_needed,
    }), 200


#POST an exercise 
@routes_bp.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        new_exercise = Exercise(
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed', False) #Defaults to false if equipment is not given 
        )

        db.session.add(new_exercise)
        db.session.commit()
        return jsonify({"id": new_exercise.id, "message": "Exercise created"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

#DELETE an exercise
@routes_bp.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'Exercise deleted'}), 200



#JOIN table routes 
#POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
#adds a specific exercise to a specific workout


@routes_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    Workout.query.get_or_404(workout_id)
    Exercise.query.get_or_404(exercise_id)

    data = request.get_json()
    try:
        new_we = WorkoutExercise(
            workout_id = workout_id,
            exercise_id = exercise_id,
            reps = data.get('reps'),
            sets = data.get('sets'),
            duration_seconds = data.get('duration_seconds')
        )
        db.session.add(new_we)
        db.session.commit()
        return jsonify({"message": "Exercise added to workout", "id": new_we.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    