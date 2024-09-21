from flask import Flask, render_template, request, redirect, url_for
from azure.storage.blob import BlobServiceClient
import os
import mlflow
import mlflow.pyfunc

app = Flask(__name__)

# Azure Blob Storage configuration
AZURE_CONNECTION_STRING = "your_connection_string"
AZURE_CONTAINER_NAME = "your_container_name"
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

# Load the model from Databricks
model_path = "/dbfs/models/fraud_detection_model"
model = mlflow.pyfunc.load_model(model_path)

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
        # Upload to Azure Blob Storage
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file.read(), overwrite=True)

        # Call the fraud detection function
        result = detect_fraud(file.filename)

        return render_template('result.html', result=result)

# Fraud detection function (replace with your own logic)
def detect_fraud(file_name):
    # Load the data from Azure Blob Storage for processing
    download_file_path = f"/tmp/{file_name}"
    with open(download_file_path, "wb") as download_file:
        blob_client = container_client.get_blob_client(file_name)
        download_file.write(blob_client.download_blob().readall())

    # Process the downloaded file
    df = pd.read_csv(download_file_path)
    frauds = df[df['Amount'] > 1000]  # Example logic
    
    if frauds.empty:
        return "No fraudulent transactions detected."
    else:
        return f"Fraudulent transactions detected: {frauds.shape[0]}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)