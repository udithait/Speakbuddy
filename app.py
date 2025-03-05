from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import whisper
import os
import soundfile as sf
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Load Whisper AI Model
model = whisper.load_model("base")  # Use 'medium' or 'large' for better accuracy

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')  # Basic frontend to test API

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"})
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return jsonify({"error": "Invalid credentials"})
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=User.query.get(session['user_id']).username)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    
    # Process audio file with Whisper AI
    result = process_speech(file_path)
    
    return jsonify(result)

def process_speech(file_path):
    try:
        # Load and process audio
        audio, samplerate = sf.read(file_path)
        
        # Run Whisper AI model for transcription
        result = model.transcribe(file_path)
        
        return {"transcription": result['text'], "confidence": "High"}  # Placeholder for AI accuracy
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)  # Create upload directory if missing
    db.create_all()  # Ensure database is created
    app.run(debug=True)
