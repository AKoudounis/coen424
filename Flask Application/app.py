from flask import Flask, request, render_template
import pandas as pd
from azure.cosmos import CosmosClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Cosmos DB client
COSMOS_DB_URL = os.getenv('COSMOS_ENDPOINT')
COSMOS_DB_KEY = os.getenv('COSMOS_KEY')
database_name = 'TransactionsDB'
container_name = 'Transactions'

client = CosmosClient(COSMOS_DB_URL, credential=COSMOS_DB_KEY)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('upload.html')

# Upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    
    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        for index, row in df.iterrows():
            item = row.to_dict()
            item['id'] = str(uuid.uuid4())  # Generate a unique ID for each item
            item['fraud_status'] = detect_fraud(item)  # Implement this function
            container.upsert_item(item)

        return f"Uploaded {file.filename} successfully to Cosmos DB!", 200
    else:
        return "File type not allowed. Please upload a CSV file.", 400

# Function to detect fraud
def detect_fraud(transaction):
    # Implement your fraud detection logic here
    return "no fraud"  # Placeholder return value

# Results route
@app.route('/results', methods=['GET'])
def get_results():
    query = 'SELECT * FROM c'  # Retrieve all items (modify as needed)
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    return {"transactions": items}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)