import sys
import json
import subprocess
import os

def run_androwarn(params):
    try:
        # Get the operation mode and tool path
        mode = params.get("mode", "").lower()
        tool_path = params.get("toolpath", "androwarn.py")  # Default to androwarn.py if not provided
        parameters = params.get("parameters", {})
        
        # Get additional parameters (APK file and any extra command-line arguments)
        apk_file = parameters.get("apk_file", "")
        additional_args = parameters.get("additional_args", "")
        
        # Build the command based on the selected mode
        command = ""
        if mode == "analyze":
            # Ensure the APK file is provided
            if not apk_file:
                raise ValueError("APK file is required for analysis mode")
            # Construct command to analyze the APK:
            # e.g., python androwarn.py -f myapp.apk [additional arguments]
            command = f"python {tool_path} -f {apk_file} {additional_args}"
        elif mode == "test":
            # Test mode: Display help information
            command = f"python {tool_path} --help"
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        
        # Execute the command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # Prepare a JSON formatted output with execution details
        output = {
            "mode": mode,
            "command": command,
            "status": "Success" if result.returncode == 0 else "Failed",
            "exit_code": result.returncode,
            "output": result.stdout.strip(),
            "error": result.stderr.strip()
        }
        
        print(json.dumps(output, indent=4))
    
    except subprocess.TimeoutExpired:
        error_output = {
            "error": "Command timed out after 5 minutes",
            "mode": mode
        }
        print(json.dumps(error_output, indent=4))
    except Exception as e:
        error_output = {
            "error": str(e),
            "mode": mode
        }
        print(json.dumps(error_output, indent=4))

if __name__ == "__main__":
    # Ensure that JSON parameters are provided via the command line
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No parameters provided"}, indent=4))
        sys.exit(1)
        
    try:
        input_json = sys.argv[1]
        params = json.loads(input_json)
        run_androwarn(params)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}, indent=4))
        sys.exit(1)
