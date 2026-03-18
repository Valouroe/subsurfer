from statement_generator import generate_clean_statement
import requests
import json
from pathlib import Path

def auto_test():
    # Target URL for local Flask server
    url = "http://127.0.0.1:5000/upload"

    # Find the folder containing this script and point to the test-csv subfolder
    file, sub_names =generate_clean_statement() # Generate the clean statement before testing

    BASE_DIR = Path(__file__).resolve().parent
    file_path = BASE_DIR / "test-csv" / "generated_account.csv"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    data = response.json()

    # Assertions check if the code actually did what we expected
    assert data["success"] is True
    assert data["filename"] == "generated_account.csv"
    assert data["subscription_data"] is not None

    print(f"Subscription data preview:\n{json.dumps(data['subscription_data'], indent=2)}")
    print(f"Expected subscription names: {sub_names}", end="\n\n")

    assert set(sub_names).issubset(data["subscription_data"].keys()), \
        f"Missing: {set(sub_names) - set(data['subscription_data'].keys())}"
    print("All expected subscriptions were correctly identified.")

    assert set(data["subscription_data"].keys()).issubset(sub_names), \
        f"Unexpected: {set(data['subscription_data'].keys()) - set(sub_names)}"
    print("No unexpected subscriptions were included.")
    
    print("Automatic Test Passed")


if __name__ == "__main__":
    auto_test()