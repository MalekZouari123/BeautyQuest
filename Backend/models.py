from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cryptography.fernet import Fernet
import os

db = SQLAlchemy()

# Use the encryption key from the config
key = os.getenv('ENCRYPTION_KEY')
cipher_suite = Fernet(key.encode())

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.LargeBinary, nullable=False)  # Store encrypted photo as binary
    recommendations = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_photo(self, photo_path):
        with open(photo_path, 'rb') as file:
            photo_data = file.read()
        self.photo = cipher_suite.encrypt(photo_data)

    def get_photo(self):
        return cipher_suite.decrypt(self.photo)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store encrypted password
    email = db.Column(db.String(255), unique=True, nullable=False)  # New column for email
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        self.password = cipher_suite.encrypt(password.encode())

    def check_password(self, password):
        return cipher_suite.decrypt(self.password).decode() == password

    def __repr__(self):
        return f"User('{self.username}', '{self.date_created}')"

class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    price_range = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    photo_url = db.Column(db.String(200), nullable=True)  # New field for clinic photo URL
    latitude = db.Column(db.Float, nullable=True)  # New field for clinic latitude
    longitude = db.Column(db.Float, nullable=True)  # New field for clinic longitude
    procedures = db.relationship('Procedure', secondary='clinic_procedure', backref='clinics')
    url = db.Column(db.String(200), nullable=True)  # New field for clinic  URL
class Procedure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    reason = db.Column(db.Text, nullable=True)  # Adding the reason column
    price_range = db.Column(db.String(50), nullable=False)

class ClinicProcedure(db.Model):
    __tablename__ = 'clinic_procedure'
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), primary_key=True)
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedure.id'), primary_key=True)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Name of the user providing feedback
    email = db.Column(db.String(255), nullable=False)  # Email of the user
    feedback = db.Column(db.Text, nullable=False)  # Feedback content
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of when the feedback was submitted

    def __repr__(self):
        return f"Feedback('{self.name}', '{self.email}', '{self.created_at}')"