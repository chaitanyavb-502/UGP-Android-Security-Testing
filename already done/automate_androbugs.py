import sys
import json
import subprocess

def run_androbugs(params):
    try:
        mode = params.get('mode', '')
        tool_path = params['toolpath']
        parameters = params['parameters']

        if mode == 'APK':
            apk_path = parameters.get('Enter APK File', '')
            if not apk_path:
                raise ValueError("APK file path is required")

            command = f"python2 {tool_path} -f \"{apk_path}\""
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            output = {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            print(json.dumps(output))
            
        else:
            print(json.dumps({'error': f'Unsupported mode: {mode}'}))
            sys.exit(1)

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
        run_androbugs(params)
    except json.JSONDecodeError:
        print(json.dumps({'error': 'Invalid JSON input'}))
        sys.exit(1)