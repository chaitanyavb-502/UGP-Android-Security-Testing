"""
wafw00f - WAF Fingerprinting Tool (JSON Automation Script)

Usage:
    python3 automate_wafw00f_with_json_input.py input.json

Sample input.json:
{
    "target_url": "https://example.com",
    "verbose": true,
    "find_all": true,
    "no_redirect": false
}
"""

import json
import subprocess
import sys

def load_input_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Failed to load JSON input: {e}")
        sys.exit(1)

def build_command(config):
    url = config.get("target_url", "").strip()
    if not url:
        print("[!] 'target_url' field is required.")
        sys.exit(1)

    options = []

    if config.get("verbose", False):
        options.append("-v")
    if config.get("find_all", False):
        options.append("-a")
    if config.get("no_redirect", False):
        options.append("-r")

    return ["wafw00f"] + options + [url]

def run_wafw00f(command):
    print("\n[+] Running command:")
    print(" ".join(command))
    print("\n[+] Output:\n")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running wafw00f: {e}")
    except FileNotFoundError:
        print("'wafw00f' is not installed. Install it using: sudo apt install wafw00f")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 automate_wafw00f_with_json_input.py input.json")
        sys.exit(1)

    config = load_input_json(sys.argv[1])
    command = build_command(config)
    run_wafw00f(command)

if __name__ == "__main__":
    main()
