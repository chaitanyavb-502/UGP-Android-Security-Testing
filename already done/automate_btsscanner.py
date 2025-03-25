import sys
import json
import subprocess

def run_btscanner(params):
    try:
        # Get tool path from parameters (default to 'btscanner' if not configured)
        tool_path = params.get('toolpath', 'btscanner')
        
        # Construct command to launch in xterm
        command = ['xterm', '-e', tool_path]
        
        # Launch in detached mode
        process = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True  # Detach from parent process
        )
        
        # Successful launch response
        output = {
            'status': 'success',
            'message': 'Btscanner launched successfully in new terminal'
        }
        print(json.dumps(output))
        
    except FileNotFoundError as e:
        error_output = {
            'error': f"Command not found: {e.filename}",
            'recommendation': 'Ensure xterm and btscanner are installed'
        }
        print(json.dumps(error_output))
    except Exception as e:
        error_output = {
            'error': str(e),
            'traceback': str(sys.exc_info())
        }
        print(json.dumps(error_output))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No parameters provided'}))
        sys.exit(1)
        
    try:
        input_json = sys.argv[1]
        params = json.loads(input_json)
        run_btscanner(params)
    except json.JSONDecodeError:
        print(json.dumps({'error': 'Invalid JSON input'}))
        sys.exit(1)