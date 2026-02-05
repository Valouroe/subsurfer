from flask import Flask, request

app = Flask(__name__)

@app.route('/upload-csv', methods=['POST'])

def upload_csv():
    file = request.files.get('my_file')
    if not file:
        return "No file uploaded", 400
    
    return f"Received: {file.filename}"

if __name__ == '__main__':
    app.run(debug=True)