from flask import Flask, request

# Initialize Flask application
app = Flask(__name__)

# Define route for file upload
@app.route('/upload-csv', methods=['POST'])

def upload_csv():
    # Retrieve file from request
    file = request.files.get('my_file') # change 'my_file' to match the key used in the front end

    # Validate if file is present
    if not file:
        return "No file uploaded", 400
    
    # Return the filename as confirmation
    return f"Received: {file.filename}"

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)