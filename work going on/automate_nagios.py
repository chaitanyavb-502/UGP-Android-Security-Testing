import sys
import json
import requests

def run_nagios(params):
    try:
        mode = params.get("mode", "").lower()
        # Base URL for your Nagios XI instance (e.g., "http://nagiosxi.example.com")
        server_url = params.get("server_url", "http://nagiosxi.example.com")
        api_key = params.get("api_key", "")
        parameters = params.get("parameters", {})

        if not api_key:
            raise ValueError("API key is required for Nagios XI API operations")

        # Common query parameters for the API calls
        common_params = {
            "apikey": api_key,
            "pretty": "1"  # Optional: format JSON output nicely
        }
        output = None
        response = None

        if mode == "test":
            # Test mode: Retrieve basic system status to verify connectivity.
            url = f"{server_url}/nagiosxi/api/v1/system/status"
            response = requests.get(url, params=common_params)
            output = response.json()

        elif mode == "get_host":
            # Retrieve details about a specific host.
            host = parameters.get("host", "")
            if not host:
                raise ValueError("The 'host' parameter is required for get_host mode")
            url = f"{server_url}/nagiosxi/api/v1/objects/host"
            query_params = common_params.copy()
            query_params["host"] = host
            response = requests.get(url, params=query_params)
            output = response.json()

        elif mode == "get_service":
            # Retrieve details about a specific service on a host.
            host = parameters.get("host", "")
            service = parameters.get("service", "")
            if not host or not service:
                raise ValueError("Both 'host' and 'service' parameters are required for get_service mode")
            url = f"{server_url}/nagiosxi/api/v1/objects/service"
            query_params = common_params.copy()
            query_params["host"] = host
            query_params["service"] = service
            response = requests.get(url, params=query_params)
            output = response.json()

        else:
            raise ValueError(f"Unsupported mode: {mode}")

        result = {
            "mode": mode,
            "status": "Success" if response and response.status_code == 200 else "Failed",
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
        run_nagios(params)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}, indent=4))
        sys.exit(1)
