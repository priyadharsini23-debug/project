from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---- HOME ROUTE ----
@app.route('/')
def home():
    return render_template('index.html')

# ---- UPLOAD HANDLER ----
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'})
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Here, you can call your ML model / analysis function
    result = {"message": f"File {file.filename} uploaded successfully!", "filepath": filepath}

    return jsonify({'status': 'success', 'result': result})

# ---- SAMPLE SYMPTOM CHECKER API ----
@app.route('/symptom', methods=['POST'])
def symptom_check():
    data = request.json
    symptom = data.get('symptom', '')

    # Dummy logic
    if 'Fever' in symptom:
        risk = "Medium"
        advice = "Possible viral infection. Rest & hydrate."
    elif 'Chest' in symptom:
        risk = "High"
        advice = "Potential cardiac issue. Visit hospital immediately!"
    else:
        risk = "Low"
        advice = "No major risk detected."

    return jsonify({'risk': risk, 'advice': advice})

# ---- TEST ROUTE FOR GESTURE ----
@app.route('/gesture', methods=['POST'])
def gesture_detect():
    data = request.json
    gesture = data.get('gesture', 'UNKNOWN')

    # In real scenario → ML model predicts gesture here
    response = f"Detected gesture: {gesture}"
    return jsonify({'status': 'success', 'gesture': gesture, 'message': response})

# ---- RUN SERVER ----
if __name__ == "__main__":
    app.run(debug=True)
