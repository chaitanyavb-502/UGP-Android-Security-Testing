import sys
import json
import requests
import os

def run_mobsf(params):
    try:
        # Retrieve mode, server URL, API key, and additional parameters
        mode = params.get("mode", "").lower()
        server_url = params.get("server_url", "http://127.0.0.1:8000")
        api_key = params.get("api_key", "")
        parameters = params.get("parameters", {})
        
        # Prepare headers for authentication
        headers = {"Authorization": api_key}
        
        if mode == "scan":
            apk_file = parameters.get("apk_file", "")
            scan_type = parameters.get("scan_type", "apk")  # Default scan type is "apk"
            if not apk_file:
                raise ValueError("APK file is required for scan mode")
            
            # 1. Upload the APK file
            upload_url = f"{server_url}/api/v1/upload"
            if not os.path.exists(apk_file):
                raise ValueError(f"APK file not found: {apk_file}")
            with open(apk_file, "rb") as f:
                files = {"file": f}
                print("Uploading APK file...")
                upload_response = requests.post(upload_url, headers=headers, files=files)
            
            if upload_response.status_code != 200:
                raise Exception(f"File upload failed: {upload_response.text}")
            upload_result = upload_response.json()
            file_hash = upload_result.get("hash")
            if not file_hash:
                raise Exception("No hash returned from upload")
            
            # 2. Initiate a scan using the returned file hash
            scan_url = f"{server_url}/api/v1/scan"
            data = {"scan_type": scan_type, "hash": file_hash}
            print("Initiating scan...")
            scan_response = requests.post(scan_url, headers=headers, json=data)
            if scan_response.status_code != 200:
                raise Exception(f"Scan initiation failed: {scan_response.text}")
            scan_result = scan_response.json()
            
            # 3. Retrieve the scan report
            report_url = f"{server_url}/api/v1/report"
            data = {"hash": file_hash, "scan_type": scan_type, "report_type": "json"}
            print("Retrieving report...")
            report_response = requests.post(report_url, headers=headers, json=data)
            if report_response.status_code != 200:
                raise Exception(f"Report retrieval failed: {report_response.text}")
            report_result = report_response.json()
            
            output = {
                "mode": mode,
                "upload_result": upload_result,
                "scan_result": scan_result,
                "report": report_result
            }
            
        elif mode == "test":
            # Test mode: Retrieve basic server info
            info_url = f"{server_url}/api/v1/info"
            print("Retrieving MobSF server info...")
            response = requests.get(info_url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Server info retrieval failed: {response.text}")
            output = {
                "mode": mode,
                "server_info": response.json()
            }
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        
        # Print final output in JSON format
        print(json.dumps(output, indent=4))
        
    except Exception as e:
        error_output = {
            "error": str(e),
            "mode": mode
        }
        print(json.dumps(error_output, indent=4))
        
if __name__ == "__main__":
    # Ensure JSON parameters are provided via the command line
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No parameters provided"}, indent=4))
        sys.exit(1)
    try:
        input_json = sys.argv[1]
        params = json.loads(input_json)
        run_mobsf(params)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}, indent=4))
        sys.exit(1)
