from flask import Flask, request, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Load the CSV file into a DataFrame
        try:
            data = pd.read_csv(file_path)
        except Exception as e:
            return f"Error reading CSV file: {e}", 400

        # Data Analysis
        try:
            # Select numeric columns
            numeric_data = data.select_dtypes(include=['number'])
            correlation_matrix = numeric_data.corr()
            
            # Return summary information as JSON
            summary = {
                "columns": list(data.columns),
                "missing_values": data.isnull().sum().to_dict(),
                "correlation_matrix": correlation_matrix.to_dict(),
            }

            return jsonify(summary)
        except Exception as e:
            return f"Error processing data: {e}", 500

    return "File upload failed", 500

if __name__ == '__main__':
    app.run(debug=True)
