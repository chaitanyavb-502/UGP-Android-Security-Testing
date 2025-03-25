import sys
import json
import requests
import time

def run_splunk(params):
    try:
        mode = params.get("mode", "").lower()
        # Base URL for Splunk's REST API (update if needed)
        server_url = params.get("server_url", "https://localhost:8089")
        username = params.get("username", "")
        password = params.get("password", "")
        parameters = params.get("parameters", {})

        if not username or not password:
            raise ValueError("Username and password are required for Splunk operations")
        
        # Setup basic authentication and headers
        auth = (username, password)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        if mode == "test":
            # Test mode: Retrieve server info to verify connectivity.
            test_url = f"{server_url}/services/server/info?output_mode=json"
            response = requests.get(test_url, auth=auth, verify=False)
            result = {
                "mode": mode,
                "status": "Success" if response.status_code == 200 else "Failed",
                "http_status": response.status_code,
                "output": response.json()
            }
            print(json.dumps(result, indent=4))
        
        elif mode == "search":
            search_query = parameters.get("search_query", "")
            if not search_query:
                raise ValueError("search_query is required for search mode")
            
            # Create a search job using blocking mode.
            search_url = f"{server_url}/services/search/jobs?output_mode=json"
            data = {
                "search": search_query,
                "exec_mode": "blocking"  # Blocking mode waits for the job to complete
            }
            response = requests.post(search_url, auth=auth, headers=headers, data=data, verify=False)
            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to create search job: {response.text}")
            job_info = response.json()
            # The SID (search job ID) may be located in job_info; adjust as needed.
            sid = job_info.get("sid")
            if not sid and "entry" in job_info and len(job_info["entry"]) > 0:
                sid = job_info["entry"][0]["content"].get("sid")
            if not sid:
                raise Exception("Search job SID not returned")
            
            # Retrieve search results using the job SID.
            results_url = f"{server_url}/services/search/jobs/{sid}/results?output_mode=json"
            results_response = requests.get(results_url, auth=auth, verify=False)
            result = {
                "mode": mode,
                "status": "Success" if results_response.status_code == 200 else "Failed",
                "http_status": results_response.status_code,
                "search_query": search_query,
                "sid": sid,
                "output": results_response.json()
            }
            print(json.dumps(result, indent=4))
        
        else:
            raise ValueError(f"Unsupported mode: {mode}")
    
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
        run_splunk(params)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}, indent=4))
        sys.exit(1)
