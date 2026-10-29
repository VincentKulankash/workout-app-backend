from .app import app
from .models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    print('Clearing out old data...')

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print('Creating exercises...')
    pushups = Exercise(name='Push-ups', category='strength', equipment_needed = False)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    squats = Exercise(name="Squats", category="strength", equipment_needed=False)
    yoga = Exercise(name="Yoga Flow", category="flexibility", equipment_needed=True)

    db.session.add_all([pushups, running, squats, yoga])
    db.session.commit()

    print("Creating workouts...")
    workout1 = Workout(date=date(2024, 5, 1), duration_minutes=45, notes =  "Morning strength session")
    workout2 = Workout(date=date(2024, 5, 3), duration_minutes=30, notes = "Cardio day")
    
    db.session.add_all([workout1, workout2])
    db.session.commit()

    print("Creating workout exercises...")
    # Add Push-ups to Workout 1
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=pushups.id, reps=15, sets=3)
    # Add Squats to Workout 1
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=squats.id, reps=20, sets=4)
    # Add Running to Workout 2
    we3 = WorkoutExercise(workout_id=workout2.id, exercise_id=running.id, reps=1, sets=1, duration_seconds=1800)
    
    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Seeding complete! ")