# backend/app.py

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# --- Config ---
UPLOAD_FOLDER = 'backend/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# --- Flask App Setup ---
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Load the trained model ---
model = load_model('model/model.h5')
print("✅ Model loaded")

# --- Class Labels (make sure same order as training) ---
class_labels = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

# --- Helper: Check file type ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Routes ---
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Preprocess the image
        img = load_img(filepath, target_size=(64, 64))
        img = img_to_array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        # Predict
        predictions = model.predict(img)
        predicted_class = class_labels[np.argmax(predictions)]

        return jsonify({
            'predicted_class': predicted_class,
            'confidence': float(np.max(predictions))
        })
    
    return jsonify({'error': 'Invalid file format'}), 400

# --- Start the server ---
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
