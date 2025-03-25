import sys
import json
import requests
import os
import base64

def run_virustotal(params):
    try:
        mode = params.get("mode", "").lower()
        api_key = params.get("api_key", "")
        parameters = params.get("parameters", {})
        
        if not api_key:
            raise ValueError("API key is required for VirusTotal operations")
        
        base_url = "https://www.virustotal.com/api/v3"
        headers = {
            "x-apikey": api_key
        }
        
        output = {}
        response = None
        
        if mode == "file_scan":
            file_path = parameters.get("file_path", "")
            if not file_path:
                raise ValueError("file_path is required for file_scan mode")
            if not os.path.exists(file_path):
                raise ValueError(f"File not found: {file_path}")
            
            url = f"{base_url}/files"
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = requests.post(url, headers=headers, files=files)
            output = response.json()
        
        elif mode == "url_scan":
            url_to_scan = parameters.get("url", "")
            if not url_to_scan:
                raise ValueError("url is required for url_scan mode")
            url = f"{base_url}/urls"
            # According to VT v3, the submitted URL is encoded in base64 (URL-safe, without padding)
            encoded_url = base64.urlsafe_b64encode(url_to_scan.encode()).decode().strip("=")
            data = {"url": url_to_scan}
            response = requests.post(url, headers=headers, data=data)
            output = response.json()
        
        elif mode == "get_report":
            resource_id = parameters.get("resource_id", "")
            if not resource_id:
                raise ValueError("resource_id is required for get_report mode")
            # The resource_id can be either a file hash or an encoded URL, depending on the scan type.
            url = f"{base_url}/files/{resource_id}"
            response = requests.get(url, headers=headers)
            output = response.json()
        
        elif mode == "test":
            # Test mode: retrieve info for a known IP (e.g., 8.8.8.8) as a basic connectivity test.
            url = f"{base_url}/ip_addresses/8.8.8.8"
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
        run_virustotal(params)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}, indent=4))
        sys.exit(1)
