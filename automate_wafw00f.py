import subprocess

def get_target_url():
    url = input("Enter the target URL (e.g. https://example.com): ").strip()
    return url

def get_scan_options():
    print("\nChoose any additional options (press Enter to skip):")
    options = []

    verbose = input("Enable verbose mode? (y/n): ").lower()
    if verbose == 'y':
        options.append("-v")

    find_all = input("Find all matching WAFs? (y/n): ").lower()
    if find_all == 'y':
        options.append("-a")

    no_redirect = input("Disable redirection? (y/n): ").lower()
    if no_redirect == 'y':
        options.append("-r")

    return options

def run_wafw00f(target_url, options):
    command = ["wafw00f"] + options + [target_url]

    print("\n[+] Running command:")
    print(" ".join(command))
    print("\n[+] Output:\n")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running wafw00f: {e}")
    except FileNotFoundError:
        print("❌ 'wafw00f' is not installed. Install it using: sudo apt install wafw00f")

def main():
    print("WAFW00F - Web Application Firewall Fingerprinting CLI\n")
    target_url = get_target_url()
    options = get_scan_options()
    run_wafw00f(target_url, options)

if __name__ == "__main__":
    main()
