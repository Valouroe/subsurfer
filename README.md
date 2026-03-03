# Subsurfer

Tech stack
---

    Backend: 
        Python 
    Frontend: 
        HTML5
        Javascript 
    Prerequisites:
        Git installed on your machine 
        Python 3.8 or higher 
        IDE (VS Code)
        Basic familiarity with command-line ops

What works today
---

Front End:

    - Web page displays on local server "http://127.0.0.1:5000/"
    - CSV upload button functional
    - Uploads CSV file to backend
    - Receives JSON file with subscription processing from backend
    - Processes JSON file into presentable data
    - Displays subscription data in an interactive table
    - Displays monthly, yearly, and total expenditures

Backend:

    - Server runs and integrates with frontend
    - Receives CSV file from frontend
    - Process the CSV and groups data by month and service category
    - Detects subscriptions in the data
    - Publishes processed data back to the frontend in a JSON file
    - Unit tests for functions
    - Integration test for file upload, processing, and file return

Description
---

    Subsurfer is a web application designed to help users identify recurring subscription charges 
    hidden within their bank statements. Users upload a CSV file exported from their bank, and the application 
    analyzes the transaction data to detect patterns indicating monthly subscriptions such as streaming services, 
    software licenses, gym memberships, and other recurring payments. The primary user is anyone looking to gain 
    visibility into their recurring expenses, whether to budget more effectively, cancel unused services, or 
    simply understand where their money goes each month. The core workflow is simple: upload a bank statement CSV, 
    let the system analyze it, and receive a clear breakdown of detected subscriptions with their amounts and 
    frequency.

How to run locally
---

    1. Clone the repository: git clone https://github.com/Valouroe/subsurfer.git
    2. Ensure python is installed: python – version
    3. Create a virtual environment: python -m venv venv 
    4. Activate the virtual network: On Windows: venv\Scripts\activate On Mac/Linux: source venv/bin/activate
    5. Install dependencies: pip install -r requirements.txt
    6. Run the application: python app.py

Contributions
---
Branch Naming Conventions: 

    New Features: feature/"feature name"
    Fixes: fix/"feature being fixed"
    Updates/Improvements: update/"feature being updated"



Pull request (Pull Request) rules:

    No self-merging
    At least 1 reviewer approval
    Link Pull Request to an issue

Definition of Done (DoD) for PRs:

    Builds/runs
    Tests pass (even if minimal)
    README updated if behavior/setup changed
