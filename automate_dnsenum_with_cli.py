import subprocess

def get_domain():
    domain = input("Enter the target domain: ").strip()
    return domain

def get_mode():
    print("\nSelect scan mode:")
    print("[1] Normal Scan (A, NS, MX)")
    print("[2] Full Enum Scan (--enum)")
    print("[3] No Reverse Lookup (--noreverse)")
    print("[4] Brute Force Subdomains")
    print("[5] Google Subdomain Scraping")
    print("[6] Full Monty (All of the above)\n")

    choice = input("Enter the number of your choice: ").strip()
    return choice

def run_dnsenum(domain, mode):
    command = ["dnsenum"]

    if mode == "1":
        # Basic A, NS, MX
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
        print("Invalid option selected.")
        return

    command.append(domain)

    print("\n[+] Running command:")
    print(" ".join(command))
    print("\n[+] Output:\n")
    subprocess.run(command)

def main():
    print("DNSENUM Interactive CLI")
    domain = get_domain()
    mode = get_mode()
    run_dnsenum(domain, mode)

if __name__ == "__main__":
    main()
