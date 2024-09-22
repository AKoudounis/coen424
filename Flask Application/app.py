import os
from flask import Flask, request, jsonify
import pandas as pd
from azure.cosmos import CosmosClient
from pyspark.sql import SparkSession
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    

# Initialize Spark session
spark = SparkSession.builder \
    .appName("FlaskApp") \
    .getOrCreate()

# Cosmos DB configuration
cosmos_client = CosmosClient('https://cosmosdb424.documents.azure.com/', 'COSMOS_DB_KEY')
database_name = 'TransactionsDB'
container_name = 'Transactions'
container = cosmos_client.get_database_client(database_name).get_container_client(container_name)


if __name__ == '__main__':
    app.run()