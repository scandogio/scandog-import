# ScanDog Import Action

A GitHub Action to import scanner results into the ScanDog platform. This action supports both file-based import and cloud scanner sync operations.

## Features

- **File-based Import**: Upload scan report files (JSON format) to the `/scans/import` endpoint
- **Cloud Scanner Sync**: Pull findings directly from cloud-based scanners via the `/scans/sync` endpoint
- **Automatic Configuration**: System automatically determines organization, integration, and product from workflow_id
- **Flexible Configuration**: Support for various scanner types and project identifiers
- **Authentication**: Secure API token-based authentication

## Usage

### Basic Configuration

```yaml
- name: ScanDog Import
  uses: scandogio/scandog-import@v1.0
  with:
    endpoint_type: 'sync'  # or 'import'
    workflow_id: 'workflow-123'
    scanner: 'SonarQube'
    scan_type: 'SAST'
    ci_run_id: 'ci-run-456'
    scandog_token: ${{ secrets.SCANDOG_TOKEN }}
    scandog_url: 'https://api.scandog.app'
```

### File-based Import (OSS Scanners)

Use this mode when you have a scan report file to upload (e.g., from Gosec, Trivy, Semgrep).

```yaml
- name: ScanDog Import
  uses: scandogio/scandog-import@v1.0
  with:
    endpoint_type: 'import'
    report_file: 'scan-results.json'
    workflow_id: 'workflow-123'
    scan_type: 'SAST'
    scanner: 'gosec'
    ci_run_id: 'ci-run-456'
    scandog_token: ${{ secrets.SCANDOG_TOKEN }}
    scandog_url: 'https://api.scandog.app'
```

### Cloud Scanner Sync

Use this mode to pull findings directly from cloud-based scanners (e.g., SonarQube, Snyk, Mend). The system automatically determines the organization, integration, and product from the workflow_id.

#### SonarQube/SonarCloud

```yaml
- name: ScanDog SonarQube Sync
  uses: scandogio/scandog-import@v1.0
  with:
    endpoint_type: 'sync'
    workflow_id: 'workflow-123'
    scanner: 'SonarQube'
    scan_type: 'SAST'
    ci_run_id: 'ci-run-456'
    project_key: 'my-project-key'
    scandog_token: ${{ secrets.SCANDOG_TOKEN }}
    scandog_url: 'https://api.scandog.app'
```

#### Snyk

```yaml
- name: ScanDog Snyk Sync
  uses: scandogio/scandog-import@v1.0
  with:
    endpoint_type: 'sync'
    workflow_id: 'workflow-123'
    scanner: 'Snyk'
    scan_type: 'SCA'
    ci_run_id: 'ci-run-456'
    project_id: 'snyk-project-789'
    scandog_token: ${{ secrets.SCANDOG_TOKEN }}
    scandog_url: 'https://api.scandog.app'
```

## Inputs

### Common Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `endpoint_type` | Type of endpoint: "import" or "sync" | No | "sync" |
| `workflow_id` | The workflow identifier | Yes | - |
| `scanner` | Scanner name (e.g., SonarQube, Snyk, gosec) | Yes | - |
| `scan_type` | Type of scan (SAST, SCA, etc.) | Yes | - |
| `ci_run_id` | CI/CD run identifier | Yes | - |
| `scandog_token` | API token for ScanDog authentication | Yes | - |
| `scandog_url` | Base URL of the ScanDog API | Yes | - |

### Import Endpoint Inputs

| Input | Description | Required | When |
|-------|-------------|----------|------|
| `report_file` | Path to scan results file | Yes | `endpoint_type: import` |

### Sync Endpoint Inputs

| Input | Description | Required | When |
|-------|-------------|----------|------|
| `project_key` | Project key (SonarQube/SonarCloud) | Yes* | `endpoint_type: sync` |
| `project_id` | Project ID (Snyk, Mend, etc.) | Yes* | `endpoint_type: sync` |

*Either `project_key` or `project_id` must be provided for sync operations.

**Note**: For sync operations, the system automatically determines:
- **Organization**: From the workflow_id
- **Integration**: Based on the scanner type and organization
- **Product**: Uses existing product or creates a default one

## Outputs

| Output | Description |
|--------|-------------|
| `status` | Status of the operation (success/failure) |
| `response` | Full response text from the ScanDog API |

## Examples

### Complete Workflow Example

```yaml
name: Security Scan and Import

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Security Scanner
        run: |
          # Your scanner command here
          echo '{"findings": []}' > scan-results.json
      
      - name: Import to ScanDog
        uses: scandogio/scandog-import@v1.0
        with:
          endpoint_type: 'import'
          report_file: 'scan-results.json'
          workflow_id: ${{ github.workflow }}-${{ github.run_id }}
          scan_type: 'SAST'
          scanner: 'custom-scanner'
          ci_run_id: ${{ github.run_id }}
          scandog_token: ${{ secrets.SCANDOG_TOKEN }}
          scandog_url: ${{ secrets.SCANDOG_API_URL }}

  sync-sonarqube:
    runs-on: ubuntu-latest
    steps:
      - name: Sync SonarQube Findings
        uses: scandogio/scandog-import@v1.0
        with:
          endpoint_type: 'sync'
          workflow_id: 'sonarqube-sync-${{ github.run_id }}'
          scanner: 'SonarQube'
          scan_type: 'SAST'
          ci_run_id: ${{ github.run_id }}
          project_key: 'my-project'
          scandog_token: ${{ secrets.SCANDOG_TOKEN }}
          scandog_url: ${{ secrets.SCANDOG_API_URL }}
```

## Scanner Support

### File-based Import (OSS Scanners)
- Gosec
- Trivy
- Semgrep
- opengrep
- checkov
- Bandit
- ...

### Commercial Scanner Sync
- SonarQube/SonarCloud
- Snyk
- Mend
- ...


## How It Works

### Sync Endpoint Flow
1. **Workflow ID**: Used to determine the organization
2. **Scanner**: Identifies the type of scanner integration needed
3. **Auto-detection**: System automatically finds the appropriate integration and product
4. **Project Sync**: Pulls findings using the provided project identifier
5. **Processing**: Findings are processed and stored in the database

### Automatic Configuration
- **Integration Selection**: System finds the first available integration for the scanner type in your organization
- **Product Management**: Uses existing products or creates a default one if none exist
- **Organization Security**: Ensures all operations are scoped to your organization

## Error Handling

The action will:
- Validate required parameters based on the endpoint type
- Provide clear error messages for missing or invalid parameters
- Exit with appropriate error codes on failure
- Log detailed error information for debugging

## Security

- API tokens are treated as secrets and should be stored in GitHub Secrets
- All communication with the ScanDog API uses HTTPS
- No sensitive data is logged or stored

## Troubleshooting

### Common Issues

1. **Missing Required Parameters**: Ensure all required inputs are provided for your chosen endpoint type
2. **Authentication Errors**: Verify your API token is valid and has the necessary permissions
3. **File Not Found**: Ensure the report file path is correct and the file exists
4. **No Integration Found**: Verify you have configured a scanner integration in ScanDog for the scanner type you're using
5. **Workflow Not Found**: Ensure the workflow_id exists and belongs to your organization

### Debug Mode

Enable debug logging by setting the `ACTIONS_STEP_DEBUG` secret to `true` in your repository settings.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
