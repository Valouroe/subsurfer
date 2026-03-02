from flask import Flask, request, render_template, jsonify
from category_grouping import sort_by_month, group_by_category, subscription_by_service
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# Point to the templates folder one level up
template_path = os.path.join(current_dir, '..', 'templates')

app = Flask(__name__, template_folder=template_path)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            file.save(filepath)
            print(f"File saved to: {filepath}")
            
            # Process the CSV file
            monthly_data = sort_by_month(filepath)
            print(f"Monthly data created: {len(monthly_data)} months")
            
            category_data = group_by_category(monthly_data)
            print(f"Category data created: {len(category_data)} categories")

            subscription_data = subscription_by_service(category_data)
            print(f"Subscription data created: {len(subscription_data)} subscriptions")

            return jsonify({
                'success': True,
                'filename': filename, 
                'subscription_data': dict(subscription_data) 
            }), 200
            
        except Exception as e:
            # Print full error traceback for debugging
            import traceback
            print("ERROR occurred:")
            print(traceback.format_exc())
            
            # Clean up file if processing failed
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500

    return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
