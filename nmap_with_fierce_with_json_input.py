"""
Fierce + Nmap Pipeline (JSON Automation Script)

Usage:
    python3 nmap_with_fierce_with_json_input.py input.json

Sample input.json:
{
    "domain": "example.com",
    "nmap_mode": "sV"
}
Valid nmap_mode values:
    "sS" → Stealth scan
    "sV" → Version scan
    "A"  → Aggressive scan
    "sn" → Ping scan
    ""   → Default scan (empty string)
"""

import subprocess
import re
import sys
import json

def load_input_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Failed to load JSON input: {e}")
        sys.exit(1)

def run_fierce(domain):
    print(f"\n[+] Running fierce on domain: {domain}\n")
    try:
        result = subprocess.run(['fierce', '--domain', domain], capture_output=True, text=True)
        output = result.stdout
        print(output)
        return output
    except Exception as e:
        print(f"[!] Error running fierce: {e}")
        return ""

def extract_targets(fierce_output):
    # Extract IPs and hostnames
    ips = re.findall(r'\((\d{1,3}(?:\.\d{1,3}){3})\)', fierce_output)
    hostnames = re.findall(r'Found: ([\w.-]+)\.', fierce_output)
    targets = list(set(ips + hostnames))
    print(f"\n[+] Discovered targets: {targets}\n")
    return targets

def run_nmap(targets, mode):
    print(f"\n[+] Running nmap with mode: {mode if mode else 'default'}\n")
    for target in targets:
        print(f"\n[*] Scanning {target}...\n")
        try:
            cmd = ['nmap', '-v']
            if mode:
                cmd.append(f'-{mode}')
            cmd.append(target)
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"[!] Error scanning {target}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 nmap_with_fierce_with_json_input.py input.json")
        sys.exit(1)

    config = load_input_json(sys.argv[1])
    domain = config.get("domain", "").strip()
    if not domain:
        print("[!] 'domain' field is required.")
        sys.exit(1)

    nmap_mode = config.get("nmap_mode", "").strip()

    fierce_output = run_fierce(domain)
    targets = extract_targets(fierce_output)

    if not targets:
        print("[!] No targets found. Exiting.")
        return

    run_nmap(targets, nmap_mode)

if __name__ == "__main__":
    main()
