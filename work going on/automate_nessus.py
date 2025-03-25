import sys
import json
import requests

# Disable warnings for insecure SSL (for demo purposes only)
requests.packages.urllib3.disable_warnings()

def run_nessus(params):
    try:
        mode = params.get("mode", "").lower()
        # Base URL for Nessus (adjust as needed)
        server_url = params.get("server_url", "https://localhost:8834")
        username = params.get("username", "")
        password = params.get("password", "")
        parameters = params.get("parameters", {})

        if not username or not password:
            raise ValueError("Username and password are required for Nessus operations")

        # 1. Log in to Nessus to obtain an authentication token.
        login_url = f"{server_url}/session"
        login_payload = {
            "username": username,
            "password": password
        }
        login_response = requests.post(login_url, json=login_payload, verify=False)
        if login_response.status_code != 200:
            raise Exception(f"Login failed: {login_response.text}")
        token = login_response.json().get("token")
        if not token:
            raise Exception("No token returned from login")

        # Set up headers for authenticated requests.
        headers = {
            "X-Cookie": f"token={token}",
            "Content-Type": "application/json"
        }
        output = {}

        if mode == "test":
            # Test mode: Retrieve basic server status.
            info_url = f"{server_url}/server/status"
            response = requests.get(info_url, headers=headers, verify=False)
            output = response.json()

        elif mode == "scan":
            # Scan mode: Create and launch a scan.
            target = parameters.get("target", "")
            policy_uuid = parameters.get("policy_uuid", "")
            scan_name = parameters.get("scan_name", "Automated Scan")
            if not target or not policy_uuid:
                raise ValueError("Both 'target' and 'policy_uuid' are required for scan mode")
            
            # Create the scan payload.
            scan_payload = {
                "uuid": policy_uuid,
                "settings": {
                    "name": scan_name,
                    "text_targets": target
                }
            }
            # Create scan (POST /scans)
            create_scan_url = f"{server_url}/scans"
            create_response = requests.post(create_scan_url, headers=headers, json=scan_payload, verify=False)
            if create_response.status_code not in [200, 201]:
                raise Exception(f"Failed to create scan: {create_response.text}")
            scan_id = create_response.json().get("scan", {}).get("id")
            if not scan_id:
                raise Exception("No scan ID returned after scan creation")
            
            # Launch the scan (POST /scans/{scan_id}/launch)
            launch_url = f"{server_url}/scans/{scan_id}/launch"
            launch_response = requests.post(launch_url, headers=headers, verify=False)
            if launch_response.status_code not in [200, 201]:
                raise Exception(f"Failed to launch scan: {launch_response.text}")
            output = {
                "message": "Scan created and launched successfully",
                "scan_id": scan_id,
                "launch_response": launch_response.json()
            }

        elif mode == "get_report":
            # Get report mode: Retrieve the scan report for a given scan ID.
            scan_id = parameters.get("scan_id", "")
            if not scan_id:
                raise ValueError("scan_id is required for get_report mode")
            report_url = f"{server_url}/scans/{scan_id}"
            response = requests.get(report_url, headers=headers, verify=False)
            output = response.json()

        else:
            raise ValueError(f"Unsupported mode: {mode}")

        result = {
            "mode": mode,
            "status": "Success",
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
        run_nessus(params)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}, indent=4))
        sys.exit(1)
