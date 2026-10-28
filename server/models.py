from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint

db = SQLAlchemy()

class Exercise: 
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

