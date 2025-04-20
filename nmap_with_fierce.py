import subprocess
import re

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
    # Extract IPs from lines 
    ips = re.findall(r'\((\d{1,3}(?:\.\d{1,3}){3})\)', fierce_output)

    # Extract hostnames from lines 
    hostnames = re.findall(r'Found: ([\w.-]+)\.', fierce_output)

    # Combine and deduplicate
    targets = list(set(ips + hostnames))
    print(f"\n[+] Discovered targets: {targets}\n")
    return targets

def choose_nmap_mode():
    print("Choose Nmap scan mode:")
    print("1) Stealth scan       (-sS)")
    print("2) Version scan       (-sV)")
    print("3) Aggressive scan    (-A)")
    print("4) Ping scan          (-sn)")
    print("5) Default scan       (no extra options)")
    
    choice = input("Enter choice [1-5]: ").strip()
    
    mode_map = {
        '1': '-sS',
        '2': '-sV',
        '3': '-A',
        '4': '-sn',
        '5': ''
    }
    
    return mode_map.get(choice, '')

def run_nmap(targets, mode):
    print(f"\n[+] Running nmap with mode: {mode if mode else 'default'}\n")
    for target in targets:
        print(f"\n[*] Scanning {target}...\n")
        try:
            cmd = ['nmap', '-v']
            if mode:
                cmd.append(mode)
            cmd.append(target)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"[!] Error scanning {target}: {e}")

def main():
    print("=== Fierce + Nmap Scanner ===\n")
    domain = input("Enter the domain name: ").strip()
    
    fierce_output = run_fierce(domain)
    targets = extract_targets(fierce_output)
    
    if not targets:
        print("[!] No targets found. Exiting.")
        return

    mode = choose_nmap_mode()
    run_nmap(targets, mode)

if __name__ == "__main__":
    main()
