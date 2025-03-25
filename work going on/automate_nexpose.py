import sys
import json
import requests
import urllib3

# Disable warnings for self-signed certificates (for testing purposes)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_nexpose(params):
    try:
        mode = params.get('mode', '').lower()
        # Base URL for your Nexpose instance
        server_url = params.get('server_url', 'https://nexpose.example.com')
        username = params.get('username', '')
        password = params.get('password', '')
        parameters = params.get('parameters', {})

        if not username or not password:
            raise ValueError("Username and password are required for authentication")
        
        # Setup basic authentication
        auth = (username, password)
        output = {}
        response = None

        if mode == 'test':
            # Retrieve basic system info: GET /api/3/system
            url = f"{server_url}/api/3/system"
            response = requests.get(url, auth=auth, verify=False)
            output = response.json()

        elif mode == 'scan':
            # Initiate a scan for a specific site.
            # Required parameter: site_id (string)
            site_id = parameters.get('site_id', '')
            if not site_id:
                raise ValueError("site_id is required for scan mode")
            # Endpoint: POST /api/3/sites/{site_id}/scans
            url = f"{server_url}/api/3/sites/{site_id}/scans"
            # In this example, we’re not passing extra JSON data; adjust if needed.
            response = requests.post(url, json={}, auth=auth, verify=False)
            output = response.json()

        elif mode == 'get_report':
            # Retrieve a scan report by scan_id.
            # Required parameter: scan_id (string)
            scan_id = parameters.get('scan_id', '')
            if not scan_id:
                raise ValueError("scan_id is required for get_report mode")
            # Endpoint: GET /api/3/scans/{scan_id}/report?format=json
            url = f"{server_url}/api/3/scans/{scan_id}/report?format=json"
            response = requests.get(url, auth=auth, verify=False)
            output = response.json()

        else:
            raise ValueError(f"Unsupported mode: {mode}")

        result = {
            "mode": mode,
            "status": "Success" if response and response.status_code in range(200, 300) else "Failed",
            "http_status": response.status_code if response else None,
            "output": output
        }
        print(json.dumps(result, indent=4))

    except Exception as e:
        error_output = {
            "error": str(e),
            "mode": mode
        }
        print(json.dumps(error_output, indent=4))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No parameters provided"}, indent=4))
        sys.exit(1)
    try:
        input_json = sys.argv[1]
        params = json.loads(input_json)
        run_nexpose(params)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}, indent=4))
        sys.exit(1)
