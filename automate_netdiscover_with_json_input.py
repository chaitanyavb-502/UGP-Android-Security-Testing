"""
Netdiscover - ARP Reconnaissance Automation Script using JSON Input

Usage:
    sudo python3 automate_netdiscover_with_json_input.py input.json

Sample input.json:
{
    "interface": "eth0",
    "scan_mode": "2",             # "1" = auto, "2" = custom IP range, "3" = passive
    "custom_range": "192.168.1.0/24",
    "fast_mode": true,
    "hardcore_mode": false
}
"""

import json
import sys
import os
import subprocess

def load_input_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Failed to load JSON input: {e}")
        sys.exit(1)

def build_command(data):
    iface = data.get("interface", "").strip()
    scan_mode = data.get("scan_mode", "").strip()
    custom_range = data.get("custom_range", "").strip()
    fast_mode = data.get("fast_mode", False)
    hardcore_mode = data.get("hardcore_mode", False)

    if not iface or not scan_mode:
        print("[!] 'interface' and 'scan_mode' fields are required.")
        sys.exit(1)

    command = ["netdiscover", "-i", iface]

    if fast_mode:
        command.append("-f")
    if hardcore_mode:
        command.append("-S")

    if scan_mode == "2":
        if not custom_range:
            print("[!] 'custom_range' is required when scan_mode is '2'.")
            sys.exit(1)
        command += ["-r", custom_range]
    elif scan_mode == "3":
        command.append("-p")

    return command

def run_netdiscover(command):
    print("\n[+] Running command:")
    print(" ".join(command))
    print("\n[+] Output:\n")

    try:
        subprocess.run(command)
    except FileNotFoundError:
        print("'netdiscover' is not installed. Install it using: sudo apt install netdiscover")
    except Exception as e:
        print(f"Error running netdiscover: {e}")

def main():
    if os.geteuid() != 0:
        print("[!] Script requires root privileges. Relaunching with sudo...\n")
        os.execvp("sudo", ["sudo", "python3"] + sys.argv)

    if len(sys.argv) != 2:
        print("Usage: sudo python3 automate_netdiscover_with_json_input.py input.json")
        sys.exit(1)

    input_data = load_input_json(sys.argv[1])
    command = build_command(input_data)
    run_netdiscover(command)

if __name__ == "__main__":
    main()
