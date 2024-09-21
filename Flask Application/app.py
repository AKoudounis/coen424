import os
from flask import Flask, request, jsonify
import pandas as pd
from azure.cosmos import CosmosClient
from pyspark.sql import SparkSession
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("FlaskApp") \
    .getOrCreate()

# Cosmos DB configuration
cosmos_client = CosmosClient('https://cosmosdb424.documents.azure.com/', 'COSMOS_DB_KEY')
database_name = 'TransactionsDB'
container_name = 'Transactions'
container = cosmos_client.get_database_client(database_name).get_container_client(container_name)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file)

    # Process and predict fraud (implement your own logic)
    results = []
    for index, row in df.iterrows():
        features = prepare_features(row)  # Implement this function
        prediction = loaded_model.predict(features)  # Load your model as needed
        results.append({"transaction_id": row["transaction_id"], "is_fraud": prediction})

    # Insert results into Cosmos DB
    for result in results:
        container.upsert_item(result)

    return jsonify({"message": "File processed successfully", "results": results}), 200

def prepare_features(row):
    # Implement this based on your model's input requirements
    return row.to_dict()  # Modify as needed

if __name__ == '__main__':
    app.run(debug=True)