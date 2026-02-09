from flask import Flask, request, jsonify
import pandas as pd
import io

# Initialize Flask application
app = Flask(__name__)

# Define route for file upload
@app.route('/upload-csv', methods=['POST'])

def upload_csv():
    # Retrieve file from request
    file = request.files.get('my_file') # change 'my_file' to match the key used in the front end

    # Validate if file is present
    if not file:
        return jsonify({"error": "No file found"}), 400

    try:
        #Read the file stream into a DataFrame
        df = pd.read_csv(io.BytesIO(file.read()))

        # Get row count and column names
        row_count = len(df)
        columns = df.columns.tolist()

        # Return a JSON response instead of a plain string
        return jsonify({
            "status": "success",
            "filename": file.filename,
            "rows_processed": row_count,
            "headers": columns
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)