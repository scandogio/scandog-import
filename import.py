import os
import requests

# Assigning environment variables
CI_RUN_ID = os.getenv("CI_RUN_ID")
REPORT_FILE = os.getenv("REPORT_FILE")
WORKFLOW_ID = os.getenv("WORKFLOW_ID")
SCAN_TYPE = os.getenv("SCAN_TYPE")
SCANNER = os.getenv("SCANNER")
BACKEND_API_TOKEN = os.getenv("BACKEND_API_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL")

# Constructing the URL
url = f"{BACKEND_URL}/scans/import"

# Constructing the request headers
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {BACKEND_API_TOKEN}"
}

# Constructing the form data
form_data = {
    "workflowID": WORKFLOW_ID,
    "cirunid": CI_RUN_ID,
    "scan_type": SCAN_TYPE,
    "scanner": SCANNER
}

# Add file to form data if it exists
files = None
if REPORT_FILE and os.path.exists(REPORT_FILE):
    files = {
        "file": ("report.json", open(REPORT_FILE, "rb"), "application/json")
    }

try:
    # Making the request
    response = requests.post(
        url,
        headers=headers,
        data=form_data,
        files=files
    )
    
    # Ensure the file is closed if it was opened
    if files:
        files["file"][1].close()
    
    # Check response status
    response.raise_for_status()
    
    print("Success:", response.json())
    
except requests.exceptions.RequestException as e:
    print("Error:", str(e))
    if hasattr(e.response, 'text'):
        print("Response:", e.response.text)
    exit(1)
except Exception as e:
    print("Unexpected error:", str(e))
    exit(1)
