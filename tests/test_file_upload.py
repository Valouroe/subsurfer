import requests
from pathlib import Path

def test_csv_upload():
    # Target URL for local Flask server
    url = "http://127.0.0.1:5000/upload-csv"

    # Find the folder containing this script and point to the test-csv subfolder
    BASE_DIR = Path(__file__).resolve().parent
    file_path = BASE_DIR / "test-csv" / "test-Statement.csv"
    
    with open(file_path, 'rb') as f:
        files = {'my_file': f} # 'my_file' should match the key expected by the server
        response = requests.post(url, files=files)
    
    data = response.json()

    # Assertions check if the code actually did what we expected
    assert data["status"] == "success"
    assert data["filename"] == "test-Statement.csv"
    assert "rows_processed" in data
    
    print("Test Passed: File uploaded and filename acknowledged.")

if __name__ == "__main__":
    try:
        test_csv_upload()
    except Exception as e:
        print(f"Test Failed: {e}")