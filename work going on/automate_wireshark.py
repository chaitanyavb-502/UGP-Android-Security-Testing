import sys
import json
import subprocess
import os

def run_wireshark(params):
    try:
        mode = params.get('mode', '').lower()
        # Default to tshark if no toolpath provided
        tool_path = params.get('toolpath', 'tshark')
        parameters = params.get('parameters', {})

        command = ""
        if mode == 'capture':
            interface = parameters.get('interface', '')
            duration = parameters.get('duration', '')
            output_file = parameters.get('output_file', '')
            if not interface or not duration or not output_file:
                raise ValueError("For capture mode, 'interface', 'duration', and 'output_file' are required")
            # The '-a duration:<seconds>' option tells tshark to stop after <seconds>
            command = f"{tool_path} -i {interface} -a duration:{duration} -w {output_file}"
        elif mode == 'test':
            # Test mode: Display tshark version info
            command = f"{tool_path} -v"
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        # Execute the command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600
        )

        # Format comprehensive output
        output = {
            'mode': mode,
            'command': command,
            'status': 'Success' if result.returncode == 0 else 'Failed',
            'exit_code': result.returncode,
            'output': result.stdout.strip(),
            'error': result.stderr.strip()
        }
        print(json.dumps(output, indent=4))

    except subprocess.TimeoutExpired:
        error_output = {
            'error': "Command timed out",
            'mode': mode
        }
        print(json.dumps(error_output, indent=4))
    except Exception as e:
        error_output = {
            'error': str(e),
            'mode': mode
        }
        print(json.dumps(error_output, indent=4))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No parameters provided"}, indent=4))
        sys.exit(1)
    try:
        input_json = sys.argv[1]
        params = json.loads(input_json)
        run_wireshark(params)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}, indent=4))
        sys.exit(1)
