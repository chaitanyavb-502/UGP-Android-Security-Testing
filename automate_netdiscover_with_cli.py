import os
import sys
import subprocess

if os.geteuid() != 0:
    print("[!] Script requires root privileges. Relaunching with sudo...\n")
    os.execvp("sudo", ["sudo", "python3"] + sys.argv)

def get_interface():
    iface = input("Enter network interface (e.g. eth0, wlan0): ").strip()
    return iface

def get_scan_mode():
    print("\nChoose Scan Mode:")
    print("1. Auto scan (common local networks)")
    print("2. Custom IP range")
    print("3. Passive sniffing only")

    choice = input("Enter your choice (1/2/3): ").strip()
    return choice

def get_custom_range():
    return input("Enter custom IP range (e.g. 192.168.1.0/24): ").strip()

def get_extra_flags():
    print("\nEnable optional flags? (press Enter to skip each):")
    fast_mode = input("Enable fast mode? (-f) (y/n): ").lower() == 'y'
    hardcore_mode = input("Enable hardcore mode? (-S) (y/n): ").lower() == 'y'

    flags = []
    if fast_mode:
        flags.append("-f")
    if hardcore_mode:
        flags.append("-S")
    return flags

def run_netdiscover(command):
    print("\n[+] Running command:")
    print(" ".join(command))
    print("\n[+] Output:\n")

    try:
        subprocess.run(command)
    except FileNotFoundError:
        print("'netdiscover' is not installed. Install it using: sudo apt install netdiscover")
    except Exception as e:
        print(f"Error running netdiscover: {e}")

def main():
    print("Netdiscover - ARP Reconnaissance CLI")

    iface = get_interface()
    scan_mode = get_scan_mode()
    flags = get_extra_flags()

    command = ["netdiscover", "-i", iface] + flags

    if scan_mode == "2":
        ip_range = get_custom_range()
        command += ["-r", ip_range]
    elif scan_mode == "3":
        command.append("-p")

    run_netdiscover(command)

if __name__ == "__main__":
    main()
