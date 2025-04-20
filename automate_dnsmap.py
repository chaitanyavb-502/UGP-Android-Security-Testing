import os
import sys
import subprocess

# Relaunch with sudo if not root
if os.geteuid() != 0:
    print("[!] Script requires root privileges. Relaunching with sudo...\n")
    os.execvp("sudo", ["sudo", "python3"] + sys.argv)

def get_target_domain():
    return input("Enter the target domain (e.g., example.com): ").strip()

def get_wordlist_option():
    use_wordlist = input("Do you want to use a custom wordlist? (y/n): ").lower() == 'y'
    wordlist = ""
    if use_wordlist:
        wordlist = input("Enter the path to the wordlist file: ").strip()
    return wordlist

def get_result_options():
    print("\nChoose result format:")
    print("1. Regular text file")
    print("2. CSV format")
    print("3. Both regular text and CSV formats")
    
    choice = input("Enter your choice (1/2/3): ").strip()
    return choice

def get_extra_flags():
    print("\nEnable optional flags? (press Enter to skip each):")
    delay = input("Enter delay between requests in milliseconds (default is 10ms): ").strip()
    ips_to_ignore = input("Enter IP addresses to ignore (comma separated): ").strip()

    flags = []
    if delay:
        flags.append(f"-d {delay}")
    if ips_to_ignore:
        flags.append(f"-i {ips_to_ignore}")
    return flags

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
    print("dnsmap - Subdomain Bruteforce Scan CLI")

    domain = get_target_domain()
    wordlist = get_wordlist_option()
    result_format = get_result_options()
    flags = get_extra_flags()

    command = ["dnsmap", domain] + flags

    if wordlist:
        command += ["-w", wordlist]
    
    if result_format == "1":
        result_file = input("Enter file path to save results (text format): ").strip()
        command += ["-r", result_file]
    elif result_format == "2":
        result_file = input("Enter file path to save results (CSV format): ").strip()
        command += ["-c", result_file]
    elif result_format == "3":
        result_file_text = input("Enter file path to save results (text format): ").strip()
        result_file_csv = input("Enter file path to save results (CSV format): ").strip()
        command += ["-r", result_file_text, "-c", result_file_csv]

    run_dnsmap(command)

if __name__ == "__main__":
    main()
