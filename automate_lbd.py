import subprocess

def get_domain():
    domain = input("Enter the target domain: ").strip()
    return domain

def confirm_scan(domain):
    print(f"\nYou're about to run Load Balancer Detection on: {domain}")
    confirm = input("Proceed? (y/n): ").lower()
    return confirm == 'y'

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
    print("LBD - Load Balancer Detection CLI\n")
    domain = get_domain()
    if confirm_scan(domain):
        run_lbd(domain)
    else:
        print("Aborted.")

if __name__ == "__main__":
    main()
