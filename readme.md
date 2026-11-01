# Workout Tracker API

## Project Description
A RESTful backend API built with Flask, SQLAlchemy, Flask-Migrate, and Marshmallow. This application allows personal trainers to create a library of reusable exercises, log workout sessions, and assign specific exercises to workouts with detailed metrics (reps, sets, or duration). The API features robust data integrity through database constraints, model validations, and schema validations, alongside nested JSON serialization.

## Installation & Database Setup
To get the application running locally, clone the repository and navigate into the project folder:
`git clone <your-repo-url>` and `cd workout-app-backend`

Next, create and activate a Python virtual environment, then install the required dependencies:
`python3 -m venv venv`
`source venv/bin/activate` (On Windows use `venv\Scripts\activate`)
`pip install -r requirements.txt`

Once dependencies are installed, apply the database migrations to create the SQLite database tables:
`flask --app server.app db upgrade head`

Finally, populate the database with example data by running the seed script:
`python3 -m server.seed`

## Run Instructions
To start the Flask development server, run the following command from the root directory:
`flask --app server.app run --port 5555`

The API will be available at `http://127.0.0.1:5555`.

## API Endpoints

### Workouts
- `GET /workouts` - List all workouts.
- `GET /workouts/<id>` - Get a single workout. Includes a nested list of associated exercises.
- `POST /workouts` - Create a new workout. Requires `date` and `duration_minutes`.
- `DELETE /workouts/<id>` - Delete a workout. Cascades to delete associated WorkoutExercises.

### Exercises
- `GET /exercises` - List all exercises.
- `GET /exercises/<id>` - Get a single exercise. Includes a nested list of associated workouts.
- `POST /exercises` - Create a new exercise. Requires `name` and `category`.
- `DELETE /exercises/<id>` - Delete an exercise. Cascades to delete associated WorkoutExercises.

### Join Table
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` - Add an exercise to a workout, including reps, sets, or duration.

## Example Requests
To create a workout, send a POST request to `/workouts` with this JSON body:
{ "date": "2024-05-15", "duration_minutes": 60, "notes": "Intense leg day" }

To add an exercise to a workout, send a POST request to `/workouts/1/exercises/2/workout_exercises` with this JSON body:
{ "reps": 12, "sets": 3 }