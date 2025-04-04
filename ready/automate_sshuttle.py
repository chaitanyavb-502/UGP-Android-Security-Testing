import sys
import json
import subprocess
import os

def run_sshuttle(params):
    try:
        mode = params.get("mode", "").lower()
        # Default to 'sshuttle' if no toolpath is provided
        tool_path = params.get("toolpath", "sshuttle")
        parameters = params.get("parameters", {})
        command = ""

        if mode in ["run", "daemon"]:
            # For run/daemon modes, require ssh_user, ssh_host, and subnets.
            ssh_user = parameters.get("ssh_user", "")
            ssh_host = parameters.get("ssh_host", "")
            subnets = parameters.get("subnets", "")
            ssh_port = parameters.get("ssh_port", "")  # Optional SSH port
            additional_args = parameters.get("additional_args", "")

            if not ssh_user or not ssh_host or not subnets:
                raise ValueError("ssh_user, ssh_host, and subnets are required for run/daemon mode")

            if ssh_port:
                connection = f"{ssh_user}@{ssh_host}:{ssh_port}"
            else:
                connection = f"{ssh_user}@{ssh_host}"

            # Construct the sshuttle command.
            # sshuttle -r user@host 0/0 --dns
            command = f"{tool_path} -r {connection} {subnets} {additional_args}"

            if mode == "run":
                # Run in foreground (blocking)
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                output = {
                    "mode": mode,
                    "command": command,
                    "status": "Success" if result.returncode == 0 else "Failed",
                    "exit_code": result.returncode,
                    "output": result.stdout.strip(),
                    "error": result.stderr.strip()
                }
            else:
                # Daemon mode: run in background using Popen
                # Detach from parent process using preexec_fn=os.setpgrp
                proc = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    preexec_fn=os.setpgrp,
                    text=True
                )
                output = {
                    "mode": mode,
                    "command": command,
                    "status": "Started in daemon mode",
                    "pid": proc.pid
                }

        elif mode == "test":
            # Test mode: display sshuttle version information.
            command = f"{tool_path} --version"
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            output = {
                "mode": mode,
                "command": command,
                "status": "Success" if result.returncode == 0 else "Failed",
                "exit_code": result.returncode,
                "output": result.stdout.strip(),
                "error": result.stderr.strip()
            }

        elif mode == "stop":
            # Stop mode: attempt to kill running sshuttle processes.
            # This uses pkill to kill all processes with 'sshuttle -r' in the command line.
            command = "pkill -f 'sshuttle -r'"
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = {
                "mode": mode,
                "command": command,
                "status": "Stop command executed",
                "exit_code": result.returncode,
                "output": result.stdout.strip(),
                "error": result.stderr.strip()
            }
        else:
            raise ValueError(f"Unsupported mode: {mode}")

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
        run_sshuttle(params)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}, indent=4))
        sys.exit(1)
