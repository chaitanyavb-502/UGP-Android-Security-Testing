"""
LBD (Load Balancer Detection) Automation Script with JSON Input

Usage:
    python3 automate_lbd_with_json_input.py input.json

Sample input.json:
{
    "domain": "example.com"
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

def run_lbd(domain):
    command = ["lbd", domain]
    
    print("\n[+] Running command:")
    print(" ".join(command))
    print("\n[+] Output:\n")
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running lbd: {e}")
    except FileNotFoundError:
        print("'lbd' is not installed. Install it using: sudo apt install lbd")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 automate_lbd_with_json_input.py input.json")
        sys.exit(1)

    input_data = load_input_json(sys.argv[1])
    domain = input_data.get("domain", "").strip()

    if not domain:
        print("[!] 'domain' field is required in the input JSON.")
        sys.exit(1)

    print(f"[+] Starting Load Balancer Detection on: {domain}")
    run_lbd(domain)

if __name__ == "__main__":
    main()
