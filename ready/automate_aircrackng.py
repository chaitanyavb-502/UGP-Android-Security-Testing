import sys
import json
import subprocess
import tempfile
import os

def run_aircrack(params):
    try:
        mode = params.get('mode', '').lower()
        tool_path = params['toolpath']
        parameters = params['parameters']
        
        # Security Note: Consider using environment variables for password in production
        SUDO_PASSWORD = "12345"  # Replace with your actual password
        
        handshake_file = parameters.get('handshake_file', '')
        wordlist = parameters.get('wordlist', '')
        bssid = parameters.get('bssid', '')
        if not handshake_file or not wordlist or not bssid:
            raise ValueError("Handshake file, wordlist, and BSSID are required")

        command_map = {
            'crack': f"sudo {tool_path} -b {bssid} -w {wordlist} {handshake_file}",
            'test': f"{tool_path} --help"
        }

        if mode not in command_map:
            raise ValueError(f"Unsupported mode: {mode}")

        command = command_map[mode]
        use_sudo = 'sudo' in command

        if use_sudo:
            # Create secure temporary expect script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.exp', delete=False) as f:
                script_content = f"""#!/usr/bin/expect -f
set timeout 300
spawn {command}
expect {{
    "password" {{ send "{SUDO_PASSWORD}\\r"; exp_continue }}
    eof
}}
"""
                f.write(script_content)
                script_path = f.name

            # Set secure permissions
            os.chmod(script_path, 0o700)
            
            # Execute with expect
            result = subprocess.run(
                ['expect', '-f', script_path],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Cleanup temporary file
            os.unlink(script_path)
        else:
            # Execute directly for non-sudo commands
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )

        # Format comprehensive output
        output = {
            'mode': mode,
            'command': command,
            'status': 'Success' if result.returncode == 0 else 'Failed',
            'exit_code': result.returncode,
            'output': result.stdout,
            'error': result.stderr
        }
        
        print(json.dumps(output))

    except subprocess.TimeoutExpired:
        error_output = {
            'error': "Command timed out after 5 minutes",
            'mode': mode
        }
        print(json.dumps(error_output))
    except Exception as e:
        error_output = {
            'error': str(e),
            'traceback': str(sys.exc_info()),
            'mode': mode
        }
        print(json.dumps(error_output))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No parameters provided'}))
        sys.exit(1)
        
    try:
        input_json = sys.argv[1]
        params = json.loads(input_json)
        run_aircrack(params)
    except json.JSONDecodeError:
        print(json.dumps({'error': 'Invalid JSON input'}))
        sys.exit(1)
