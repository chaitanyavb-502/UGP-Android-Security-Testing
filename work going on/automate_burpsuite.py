import sys
import json
import requests

def run_burpsuite(params):
    try:
        # Get the mode, server URL, API key, and additional parameters
        mode = params.get("mode", "").lower()
        server_url = params.get("server_url", "http://127.0.0.1:8080")
        api_key = params.get("api_key", "")
        parameters = params.get("parameters", {})

        if not api_key:
            raise ValueError("API key is required for Burp Suite operations")

        # Setup headers with API key for Bearer token authentication (adjust as needed)
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        output = {}
        response = None

        if mode == "scan":
            target = parameters.get("target", "")
            if not target:
                raise ValueError("Target is required for scan mode")
            # Assume endpoint: POST /api/v1/scan with JSON body {"target": target}
            url = f"{server_url}/api/v1/scan"
            data = {"target": target}
            response = requests.post(url, headers=headers, json=data)
            output = response.json()

        elif mode == "get_report":
            scan_id = parameters.get("scan_id", "")
            if not scan_id:
                raise ValueError("Scan ID is required for get_report mode")
            # Assume endpoint: GET /api/v1/report/{scan_id}
            url = f"{server_url}/api/v1/report/{scan_id}"
            response = requests.get(url, headers=headers)
            output = response.json()

        elif mode == "test":
            # Test mode: Retrieve basic server info (assume endpoint: GET /api/v1/info)
            url = f"{server_url}/api/v1/info"
            response = requests.get(url, headers=headers)
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
        run_burpsuite(params)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}, indent=4))
        sys.exit(1)
