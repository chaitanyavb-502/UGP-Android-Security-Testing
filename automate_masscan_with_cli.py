import subprocess

def run_masscan():
    print("=== Masscan Automated Scanner ===")
    target = input("Enter the target IP or subnet: ")
    ports = input("Enter ports to scan (e.g., 0-65535 or 80,443): ")
    rate = input("Enter scan rate (packets per second, e.g., 1000): ")

    cmd = [
        "sudo", "masscan",
        "-p", ports,
        target,
        "--rate", rate
    ]

    print("\nRunning Masscan...\n")
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("=== Masscan Output ===")
        print(result.stdout)
        if result.stderr:
            print("=== Masscan Errors (if any) ===")
            print(result.stderr)
    except Exception as e:
        print(f"Error running Masscan: {e}")

if __name__ == "__main__":
    run_masscan()
