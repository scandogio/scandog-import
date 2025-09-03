import os
import requests

# Assigning environment variables
CI_RUN_ID = os.getenv("CI_RUN_ID")
REPORT_FILE = os.getenv("REPORT_FILE")
WORKFLOW_ID = os.getenv("WORKFLOW_ID")
PRODUCT_ID = os.getenv("PRODUCT_ID")
SCAN_TYPE = os.getenv("SCAN_TYPE")
SCANNER = os.getenv("SCANNER")
PROJECT_KEY = os.getenv("PROJECT_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
SCANDOG_TOKEN = os.getenv("SCANDOG_TOKEN")
SCANDOG_URL = os.getenv("SCANDOG_URL")
ENDPOINT_TYPE = os.getenv("ENDPOINT_TYPE", "sync")  # Default to sync

# Determine which endpoint to use
if ENDPOINT_TYPE.lower() == "import":
    # Use import endpoint for file-based scans
    url = f"{SCANDOG_URL}/scans/import"
    
    # Constructing the request headers
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {SCANDOG_TOKEN}"
    }
    
    # Constructing the form data for import
    form_data = {
        "workflow_id": WORKFLOW_ID,
        "ci_run_id": CI_RUN_ID,
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

else:
    # Use sync endpoint for cloud-based scanners
    url = f"{SCANDOG_URL}/scans/sync"
    
    # Constructing the request headers
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {SCANDOG_TOKEN}"
    }
    
    # Validate required parameters for sync
    if not PROJECT_KEY and not PROJECT_ID:
        print("Error: Either PROJECT_KEY or PROJECT_ID must be provided for sync endpoint")
        exit(1)
    
    # Constructing the form data for sync
    form_data = {
        "workflow_id": WORKFLOW_ID,
        "ci_run_id": CI_RUN_ID,
        "scanner": SCANNER,
        "scan_type": SCAN_TYPE
    }
    
    # Add optional project identifiers
    if PROJECT_KEY:
        form_data["project_key"] = PROJECT_KEY
    if PROJECT_ID:
        form_data["project_id"] = PROJECT_ID
    
    try:
        # Making the request
        response = requests.post(
            url,
            headers=headers,
            data=form_data
        )
        
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
