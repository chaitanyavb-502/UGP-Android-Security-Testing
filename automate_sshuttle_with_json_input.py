"""
sshuttle - Transparent Proxy via SSH (JSON Automation Script)

Usage:
    sudo python3 automate_sshuttle_with_json_input.py input.json

Sample input.json:
{
    "remote": "user@remotehost:22",
    "subnets": ["0.0.0.0/0"],
    "excludes": ["192.168.1.0/24"],
    "dns": true,
    "auto_nets": false,
    "auto_hosts": true,
    "daemon": false
}
"""

import json
import subprocess
import sys
import os

def load_input_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Failed to load JSON input: {e}")
        sys.exit(1)

def build_command(data):
    remote = data.get("remote", "").strip()
    subnets = data.get("subnets", [])
    excludes = data.get("excludes", [])
    dns = data.get("dns", False)
    auto_nets = data.get("auto_nets", False)
    auto_hosts = data.get("auto_hosts", False)
    daemon = data.get("daemon", False)

    if not remote or not subnets:
        print("[!] 'remote' and 'subnets' fields are required.")
        sys.exit(1)

    cmd = ["sudo", "sshuttle", "-r", remote]

    if dns:
        cmd.append("--dns")
    if auto_nets:
        cmd.append("--auto-nets")
    if auto_hosts:
        cmd.append("--auto-hosts")
    if daemon:
        cmd.append("--daemon")

    for ex in excludes:
        if ex.strip():
            cmd.extend(["-x", ex.strip()])

    cmd.extend([s.strip() for s in subnets if s.strip()])
    return cmd

def run_sshuttle(command):
    print("\n[+] Executing command:")
    print(" ".join(command))
    print("\n[+] Output:\n")

    try:
        subprocess.run(command)
    except FileNotFoundError:
        print("'sshuttle' is not installed. Install it via: sudo apt install sshuttle")
    except Exception as e:
        print(f"Error running sshuttle: {e}")

def main():
    if os.geteuid() != 0:
        print("[!] Script requires root privileges. Relaunching with sudo...\n")
        os.execvp("sudo", ["sudo", "python3"] + sys.argv)

    if len(sys.argv) != 2:
        print("Usage: sudo python3 automate_sshuttle_with_json_input.py input.json")
        sys.exit(1)

    input_data = load_input_json(sys.argv[1])
    command = build_command(input_data)
    run_sshuttle(command)

if __name__ == "__main__":
    main()
