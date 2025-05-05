"""
Masscan Automated Scanner using JSON Input

Usage:
    sudo python3 automate_masscan_with_json_input.py input.json

Sample input.json:
{
    "target": "192.168.1.0/24",
    "ports": "80,443",
    "rate": "1000"
}
"""

import json
import sys
import subprocess

def load_input_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Failed to load JSON input: {e}")
        sys.exit(1)

def run_masscan(target, ports, rate):
    cmd = [
        "sudo", "masscan",
        "-p", ports,
        target,
        "--rate", rate
    ]

    print("\n[+] Running Masscan...\n")
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("=== Masscan Output ===")
        print(result.stdout)
        if result.stderr:
            print("=== Masscan Errors (if any) ===")
            print(result.stderr)
    except Exception as e:
        print(f"Error running Masscan: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: sudo python3 automate_masscan_with_json_input.py input.json")
        sys.exit(1)

    input_data = load_input_json(sys.argv[1])

    target = input_data.get("target", "").strip()
    ports = input_data.get("ports", "").strip()
    rate = input_data.get("rate", "").strip()

    if not target or not ports or not rate:
        print("[!] 'target', 'ports', and 'rate' fields are required in the input JSON.")
        sys.exit(1)

    run_masscan(target, ports, rate)

if __name__ == "__main__":
    main()
