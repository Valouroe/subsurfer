import requests
from pathlib import Path
import json

def test_csv_upload_1():
    # Target URL for local Flask server
    url = "http://127.0.0.1:5000/upload"

    # Find the folder containing this script and point to the test-csv subfolder
    BASE_DIR = Path(__file__).resolve().parent
    file_path = BASE_DIR / "test-csv" / "test-Statement.csv"
    
    with open(file_path, 'rb') as f:
        files = {'file': f} # Changed from 'my_file' to 'file'
        response = requests.post(url, files=files)
    
    data = response.json()

    # Assertions check if the code actually did what we expected
    assert data["success"] == True
    assert data["filename"] == "test-Statement.csv"
    assert data["subscription_data"] is not None
    assert len(data["subscription_data"]) >= 0
    
    print("Test 1 Passed: File uploaded and filename acknowledged.")
    preview = dict(list(data['subscription_data'].items())[:2])
    print(f"Subscription data preview:\n{json.dumps(preview, indent=2)}")

def test_csv_upload_2():
    url = "http://127.0.0.1:5000/upload"

    BASE_DIR = Path(__file__).resolve().parent
    file_path = BASE_DIR / "test-csv" / "test-Statement2.csv"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    data = response.json()

    assert data["success"] == True
    assert data["filename"] == "test-Statement2.csv"
    assert data["subscription_data"] is not None
    assert len(data["subscription_data"]) >= 0
    
    print("Test 2 Passed: File uploaded and filename acknowledged.")
    preview = dict(list(data['subscription_data'].items())[:2])
    print(f"Subscription data preview:\n{json.dumps(preview, indent=2)}")

def test_csv_upload_3():
    # Target URL for local Flask server
    url = "http://127.0.0.1:5000/upload"

    BASE_DIR = Path(__file__).resolve().parent
    file_path = BASE_DIR / "test-csv" / "test-Statement3.csv"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    data = response.json()

    assert data["success"] == True
    assert data["filename"] == "test-Statement3.csv"
    assert data["subscription_data"] is not None
    assert len(data["subscription_data"]) >= 0
    
    print("Test 3 Passed: File uploaded and filename acknowledged.")
    preview = dict(list(data['subscription_data'].items())[:2])
    print(f"Subscription data preview:\n{json.dumps(preview, indent=2)}")

if __name__ == "__main__":
    try:
        test_csv_upload_1()
        test_csv_upload_2()
        test_csv_upload_3()
    except Exception as e:
        print(f"Test Failed: {e}")