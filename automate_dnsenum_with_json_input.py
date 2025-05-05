"""
DNSENUM Automation Script with JSON Input

Usage:
    python3 automate_dnsenum_with_json_input.py input.json

Sample input.json:
{
    "domain": "example.com",
    "mode": "6"
}

Mode Options:
    "1" - Normal Scan (A, NS, MX)
    "2" - Full Enum Scan (--enum)
    "3" - No Reverse Lookup (--noreverse)
    "4" - Brute Force Subdomains (--file)
    "5" - Google Subdomain Scraping (--scrap)
    "6" - Full Monty (All of the above)
"""

import json
import sys
import subprocess

def load_input_json(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"[!] Failed to load JSON input: {e}")
        sys.exit(1)

def run_dnsenum(domain, mode):
    command = ["dnsenum"]

    if mode == "1":
        # Basic A, NS, MX (no extra flags)
        pass
    elif mode == "2":
        command.append("--enum")
    elif mode == "3":
        command.append("--noreverse")
    elif mode == "4":
        command.extend(["--file", "/usr/share/dnsenum/dns.txt"])
    elif mode == "5":
        command.extend(["--scrap", "20", "--pages", "5"])
    elif mode == "6":
        command.extend(["--enum", "--file", "/usr/share/dnsenum/dns.txt", "--scrap", "20", "--pages", "5", "--noreverse"])
    else:
        print("[!] Invalid mode selected.")
        return

    command.append(domain)

    print("\n[+] Running command:")
    print(" ".join(command))
    print("\n[+] Output:\n")
    subprocess.run(command)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 automate_dnsenum_with_json_input.py input.json")
        sys.exit(1)

    input_path = sys.argv[1]
    input_data = load_input_json(input_path)

    domain = input_data.get("domain", "").strip()
    mode = input_data.get("mode", "").strip()

    if not domain or not mode:
        print("[!] Both 'domain' and 'mode' fields are required in the JSON input.")
        sys.exit(1)

    run_dnsenum(domain, mode)

if __name__ == "__main__":
    main()
