from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import mlflow
import mlflow.pyfunc

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the model from Databricks
model_path = "/dbfs/models/fraud_detection_model"  # Update this if needed
model = mlflow.pyfunc.load_model(model_path)

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

# Fraud detection function using the ML model
def detect_fraud(file_path):
    # Load the data
    df = pd.read_csv(file_path)

    # Prepare data for the model (ensure the columns match your model's expected input)
    # You may need to preprocess the DataFrame as per your model's requirements.
    # For example, if your model expects specific features:
    # df = df[['Feature1', 'Feature2', 'FeatureN']]

    # Make predictions
    predictions = model.predict(df)

    # Interpret predictions (assuming binary classification for fraud detection)
    frauds = df[predictions == 1]  # Adjust this based on how your model outputs predictions

    if frauds.empty:
        return "No fraudulent transactions detected."
    else:
        return f"Fraudulent transactions detected: {frauds.shape[0]}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
