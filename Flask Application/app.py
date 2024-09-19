from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for file upload and fraud detection
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the uploaded file for fraud detection
        result = detect_fraud(file_path)

        return render_template('result.html', result=result)

# Fraud detection function (replace with your own logic)
def detect_fraud(file_path):
    # Example: Load CSV and check if any transaction amount is > $1000 (simple logic)
    df = pd.read_csv(file_path)
    frauds = df[df['Amount'] > 1000]  # Simple example logic for detecting "fraud"
    
    if frauds.empty:
        return "No fraudulent transactions detected."
    else:
        return f"Fraudulent transactions detected: {frauds.shape[0]}"

if __name__ == '__main__':
    app.run(debug=True)