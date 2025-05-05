"""
dnsmap Automation Script with JSON Input

Usage:
    sudo python3 automate_dnsmap_with_json_input.py input.json

Sample input.json:
{
    "domain": "example.com",
    "wordlist": "/usr/share/wordlists/dnsmap.txt",
    "result_format": "3",
    "result_file_text": "output.txt",
    "result_file_csv": "output.csv",
    "delay": "20",
    "ignore_ips": "127.0.0.1,8.8.8.8"
}

result_format options:
    "1" - Save output in text file
    "2" - Save output in CSV
    "3" - Save both text and CSV
"""

import os
import sys
import json
import subprocess

def load_input_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Failed to load JSON input: {e}")
        sys.exit(1)

def run_dnsmap(command):
    print("\n[+] Running command:")
    print(" ".join(command))
    print("\n[+] Output:\n")

    try:
        subprocess.run(command)
    except FileNotFoundError:
        print("'dnsmap' is not installed. Install it using: sudo apt install dnsmap")
    except Exception as e:
        print(f"Error running dnsmap: {e}")

def main():
    # Ensure script is run with root privileges
    if os.geteuid() != 0:
        print("[!] Script requires root privileges. Relaunching with sudo...\n")
        os.execvp("sudo", ["sudo", "python3"] + sys.argv)

    if len(sys.argv) != 2:
        print("Usage: sudo python3 automate_dnsmap_with_json_input.py input.json")
        sys.exit(1)

    input_data = load_input_json(sys.argv[1])

    domain = input_data.get("domain", "").strip()
    if not domain:
        print("[!] Domain is required in input JSON.")
        sys.exit(1)

    wordlist = input_data.get("wordlist", "").strip()
    result_format = input_data.get("result_format", "").strip()
    delay = input_data.get("delay", "").strip()
    ignore_ips = input_data.get("ignore_ips", "").strip()

    command = ["dnsmap", domain]

    # Optional flags
    if delay:
        command += ["-d", delay]
    if ignore_ips:
        command += ["-i", ignore_ips]
    if wordlist:
        command += ["-w", wordlist]

    # Result output files
    if result_format == "1":
        result_file = input_data.get("result_file_text", "").strip()
        if result_file:
            command += ["-r", result_file]
    elif result_format == "2":
        result_file = input_data.get("result_file_csv", "").strip()
        if result_file:
            command += ["-c", result_file]
    elif result_format == "3":
        result_file_text = input_data.get("result_file_text", "").strip()
        result_file_csv = input_data.get("result_file_csv", "").strip()
        if result_file_text:
            command += ["-r", result_file_text]
        if result_file_csv:
            command += ["-c", result_file_csv]

    run_dnsmap(command)

if __name__ == "__main__":
    main()
