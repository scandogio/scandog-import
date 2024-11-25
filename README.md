# Import Scanner Results to ScanDog GitHub Action

This GitHub Action automates the import of scanner results into **ScanDog**, enabling seamless integration with your CI/CD pipelines. It uses a Python script to upload scanner findings to the ScanDog backend for centralized vulnerability management.

---

## Inputs

| Name                | Description                                  | Required | Example                  |
|---------------------|----------------------------------------------|----------|--------------------------|
| `report_file`       | Path to the scanner results file (JSON format). | Yes      | `results.json`         |
| `workflow_id`       | The identifier for the workflow.            | Yes      | `0123456789`           |
| `scan_type`         | The type of scan (e.g., `SAST`, `SCA`). | Yes      | `Container Scanner`               |
| `scanner`           | The name of the scanner (e.g., `trivy`, `Semgrep`). | Yes      | `depscan`          |
| `backend_api_token` | The API token for authenticating with ScanDog. | Yes      | `12345-abcde-67890`      |
| `backend_url`       | The base URL of the ScanDog API.            | Yes      | `https://[Your-instance].scandog.app` |

---

## Outputs

| Name      | Description                                          |
|-----------|------------------------------------------------------|
| `status`  | Status of the import operation (`success`/`failure`).|
| `response`| Full response text from the ScanDog API.             |

---

## Example Usage

Add the following to your GitHub Actions workflow:

```yaml
name: Import Scanner Results to ScanDog

on:
  push:
    branches:
      - main

jobs:
  import-scan-results:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Run scanner
        run: |
          # Run your scanner and save the report
          Trivy scan ... > results.json

      - name: Import results to ScanDog
        uses: scandogio/scandog-import@v1.0
        with:
          report_file: trivy-results.json
          workflow_id: 0012345679900
          scan_type: Container Scanner
          scanner: Trivy
          backend_api_token: ${{ secrets.SCANDOG_API_KEY }}
          backend_url: https://[Your-instance].scandog.app
```

## Troubleshooting
- **Authentication Issues:** Ensure the backend_api_token is correct and not expired.
- **File Errors:** Verify the report_file path and confirm it points to a valid JSON file.
- **Connection Problems:** Check the backend_url to ensure the ScanDog API is reachable from the runner.