import os
import requests

# Assigning environment variables
GITHUB_RUN_ID = os.getenv("GITHUB_RUN_ID")
REPORT_FILE = os.getenv("REPORT_FILE")
WORKFLOW_ID = os.getenv("WORKFLOW_ID")
SCAN_TYPE = os.getenv("SCAN_TYPE")
SCANNER = os.getenv("SCANNER")
BACKEND_API_TOKEN = os.getenv("BACKEND_API_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL")

# Constructing the URL
url = f"{BACKEND_URL}/scans/import/?workflowID={WORKFLOW_ID}&cirunid={GITHUB_RUN_ID}&scan_type={SCAN_TYPE}&scanner={SCANNER}"

# Constructing the request headers
headers = {
    "accept": "application/json",
    "Org-API-Key": f"{BACKEND_API_TOKEN}"
}

# Constructing the request payload
files = {
    "file": (REPORT_FILE, open(REPORT_FILE, "rb"), "application/json")
}

# Making the request
response = requests.post(url, headers=headers, files=files)

# Printing the response
print("Response:", response.text)