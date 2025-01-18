from flask import request, jsonify, redirect, url_for, session 
from app import app, db, bcrypt, google 
from models import Patient, Clinic, Procedure, User, Feedback
from ai_model import generate_recommendations, get_surgery_recommendations
import os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from cryptography.fernet import Fernet
from config import Config

# Initialize the cipher suite with the encryption key
cipher_suite = Fernet(Config.ENCRYPTION_KEY.encode())
# Helper Function to Validate File Type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# OAuth Login Route
@app.route('/oauth/login')
def oauth_login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

# OAuth Callback Route
@app.route('/auth/callback')
def authorize():
    try:
        token = google.authorize_access_token()
        user_info = google.get('userinfo').json()
        email = user_info['email']  # Get email from Google
        name = user_info.get('name', '')

        # Check if the user already exists in the database
        user = User.query.filter_by(email=email).first()

        # If the user does not exist, create a new user
        if not user:
            user = User(username=name, email=email)
            db.session.add(user)
            db.session.commit()

        # Generate JWT token for the user
        access_token = create_access_token(identity=email)  # Use email as identity
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        return jsonify({"error": f"OAuth failed: {str(e)}"}), 500

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logged out successfully'}), 200

# Protected Route Example
@app.route('/api/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}! Login Successful'}), 200


@app.route('/api/upload_photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({"error": "No photo uploaded"}), 400

    photo = request.files['photo']

    if not allowed_file(photo.filename):
        return jsonify({"error": "Invalid file type"}), 400

    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
    photo.save(photo_path)

    try:
        # Read the photo file as binary data
        with open(photo_path, 'rb') as file:
            photo_data = file.read()

        # Encrypt the binary data
        encrypted_photo = cipher_suite.encrypt(photo_data)

        # Generate recommendations
        recommendations = generate_recommendations(photo_path)

        # Save patient info and recommendations to the database
        patient = Patient(name="Sample Patient", photo=encrypted_photo, recommendations=str(recommendations))
        db.session.add(patient)
        db.session.commit()

        return jsonify({"recommendations": recommendations}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route: AI Surgery Recommendations
@app.route('/api/get_surgery_recommendations', methods=['POST'])
def get_surgery_recommendations_route():
    if 'photo' not in request.files:
        return jsonify({"error": "No photo uploaded"}), 400

    photo = request.files['photo']
    if not allowed_file(photo.filename):
        return jsonify({"error": "Invalid file type"}), 400

    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
    photo.save(photo_path)

    try:
        recommendations = get_surgery_recommendations(photo_path)
        return jsonify({"recommendations": recommendations}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route: Get Clinics
@app.route('/api/get_clinics', methods=['GET'])
def get_clinics():
    price_range = request.args.get('price_range')
    location = request.args.get('location')
    rating = request.args.get('rating', type=float)  # Get the rating parameter

    query = Clinic.query.distinct()  # Ensure unique results
    
    if price_range:
        try:
            min_price, max_price = map(int, price_range.split('-'))
            query = query.filter(Clinic.price_range.between(min_price, max_price))
        except ValueError:
            return jsonify({"error": "Invalid price range format. Use 'min-max'"}), 400
    if location:
        query = query.filter(Clinic.location.ilike(f"%{location}%"))
    if rating:
        query = query.filter(Clinic.rating >= rating)  # Filter by rating

    clinics = query.all()
    clinic_list = [{
        "name": clinic.name,
        "location": clinic.location,
        "price_range": clinic.price_range,
        "rating": clinic.rating,
        "photo_url": clinic.photo_url,
        "latitude": clinic.latitude,
        "longitude": clinic.longitude,
        "procedures_offered": [procedure.name for procedure in clinic.procedures],
        "qr_code_url": f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={clinic.url}'
    } for clinic in clinics]

    print("Clinics returned:", clinic_list)  # Add this line to log the clinics
    return jsonify({"clinics": clinic_list}), 200

# Route: Signup
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    print(f"Received data: {data}")
    username = data['username']
    email = data['email']  # Add email field
    password = data['password']
    confirm_password = data['confirm_password']

    if password != confirm_password:
        print("Passwords do not match")
        return jsonify({'message': 'Passwords do not match'}), 400

    if len(password) < 10 or not any(char.isupper() for char in password) or \
       not any(char.islower() for char in password) or not any(char.isdigit() for char in password):
        print("Password validation failed")
        return jsonify({'message': 'Password must be at least 10 characters long and include upper and lower case letters and numbers'}), 400

    # Check if the email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)  # Add email field
        db.session.add(user)
        db.session.commit()
        print("User created successfully")
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
# Route: Login with Rate Limiting
# Existing Login Route with JWT
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.email)  # Use email as identity
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Login failed'}), 401
    
# Create QR code for clinics
@app.route('/api/create_qr', methods=['POST'])
def create_qr():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    qr_code_url = f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={url}'
    return jsonify({'qr_code_url': qr_code_url}), 201

# Retrieve QR code for clinics
@app.route('/api/get_qr', methods=['GET'])
def get_qr():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    qr_code_url = f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={url}'
    return jsonify({'qr_code_url': qr_code_url}), 200

if __name__ == '__main__':
    app.run(debug=True)
    # Route: Delete Clinic by Name
@app.route('/api/delete_clinic', methods=['DELETE'])
def delete_clinic():
    data = request.get_json()
    clinic_name = data.get('name')

    if not clinic_name:
        return jsonify({"error": "Clinic name is required"}), 400

    clinic = Clinic.query.filter_by(name=clinic_name).first()
    if not clinic:
        return jsonify({"error": "Clinic not found"}), 404

    db.session.delete(clinic)
    db.session.commit()
    return jsonify({"message": f"Clinic '{clinic_name}' deleted successfully"}), 200

# Route: Delete Clinics with Empty URLs
@app.route('/api/delete_empty_url_clinics', methods=['DELETE'])
def delete_empty_url_clinics():
    clinics_with_empty_url = Clinic.query.filter(Clinic.url == None).all()
    for clinic in clinics_with_empty_url:
        db.session.delete(clinic)
    db.session.commit()
    return jsonify({"message": "Clinics with empty URLs deleted successfully"}), 200

# Route: Delete Duplicate Clinics
@app.route('/api/delete_duplicate_clinics', methods=['DELETE'])
def delete_duplicate_clinics():
    clinics = Clinic.query.all()
    unique_clinics = {}
    duplicates = []

    for clinic in clinics:
        if clinic.name not in unique_clinics:
            unique_clinics[clinic.name] = clinic
        else:
            duplicates.append(clinic)

    for duplicate in duplicates:
        db.session.delete(duplicate)

    db.session.commit()
    return jsonify({"message": "Duplicate clinics deleted successfully"}), 200
#update address of clinics 
@app.route('/api/update_clinic_address', methods=['PUT'])
def update_clinic_address():
    data = request.json
    clinic_id = data.get('id')
    new_address = data.get('address')

    clinic = Clinic.query.get(clinic_id)
    if clinic:
        clinic.location = new_address
        db.session.commit()
        return jsonify({"message": "Address updated successfully"}), 200
    else:
        return jsonify({"message": "Clinic not found"}), 404
    
@app.route('/api/update_clinic_coordinates', methods=['PUT'])
def update_clinic_coordinates():
    data = request.json
    location = data.get('location')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    clinic = Clinic.query.filter_by(location=location).first()
    if clinic:
        clinic.latitude = latitude
        clinic.longitude = longitude
        db.session.commit()
        return jsonify({"message": "Coordinates updated successfully"}), 200
    else:
        return jsonify({"message": "Clinic not found"}), 404
    
feedback_list = []

from models import Feedback  # Import the Feedback model

# Route: Submit Feedback
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    feedback_data = request.json
    name = feedback_data.get('name')
    email = feedback_data.get('email')
    feedback_content = feedback_data.get('feedback')

    if not name or not email or not feedback_content:
        return jsonify({"error": "Name, email, and feedback are required"}), 400

    try:
        # Create a new Feedback entry
        feedback = Feedback(name=name, email=email, feedback=feedback_content)
        db.session.add(feedback)
        db.session.commit()
        return jsonify({"message": "Feedback received"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route: Get All Feedback
@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    try:
        feedback_list = Feedback.query.all()
        feedback_data = [{
            "id": feedback.id,
            "name": feedback.name,
            "email": feedback.email,
            "feedback": feedback.feedback,
            "created_at": feedback.created_at
        } for feedback in feedback_list]
        return jsonify({"feedback": feedback_data}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



@app.route('/api/delete_duplicate_procedures', methods=['DELETE'])
def delete_duplicate_procedures():
    procedures = Procedure.query.all()
    unique_procedures = {}
    duplicates = []

    for procedure in procedures:
        if procedure.name not in unique_procedures:
            unique_procedures[procedure.name] = procedure
        else:
            duplicates.append(procedure)

    for duplicate in duplicates:
        db.session.delete(duplicate)

    db.session.commit()
    return jsonify({"message": "Duplicate procedures deleted successfully"}), 200



@app.route('/api/update_procedure', methods=['POST'])
def update_procedure():
    data = request.get_json()
    procedure_id = data.get('id')
    description = data.get('description')
    reason = data.get('reason')

    procedure = Procedure.query.get(procedure_id)
    if not procedure:
        return jsonify({'error': 'Procedure not found'}), 404

    procedure.description = description
    procedure.reason = reason
    db.session.commit()

    return jsonify({'message': 'Procedure updated successfully'})

@app.route('/api/get_photo/<int:patient_id>', methods=['GET'])
def get_photo(patient_id):
    try:
        # Fetch the patient record from the database
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Decrypt the photo
        decrypted_photo = cipher_suite.decrypt(patient.photo)

        # Return the decrypted photo as a response
        return (decrypted_photo, 200, {
            'Content-Type': 'image/jpeg',
            'Content-Disposition': f'attachment; filename={patient.name}_photo.jpg'
        })
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
if __name__ == '__main__':
    app.run(debug=True)