from flask import Flask
from flask_migrate import Migrate
from .config import Config
from .models import db 

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

#to run the migration use flask --app server.app db init
