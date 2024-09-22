from flask import Flask, request, render_template
import pandas as pd

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
        # Process the DataFrame (df) as needed
        return f"Uploaded {file.filename} successfully!", 200
    else:
        return "File type not allowed. Please upload a CSV file.", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)