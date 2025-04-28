import subprocess
import sys
import os

def get_remote():
    remote = input("Enter remote SSH server (user@host[:port]): ").strip()
    return remote

def get_subnets():
    subnets = input("Enter subnets to route (e.g., 0.0.0.0/0 for all, or comma-separated): ").strip()
    return subnets.split(',')

def get_excludes():
    excludes = input("Enter subnets to exclude (comma-separated, or leave blank): ").strip()
    return excludes.split(',') if excludes else []

def yes(prompt):
    return input(f"{prompt} (y/n): ").strip().lower() == 'y'

def build_command(remote, subnets, excludes, dns, auto_nets, auto_hosts, daemon):
    cmd = ["sudo", "sshuttle", "-r", remote]

    if dns:
        cmd.append("--dns")
    if auto_nets:
        cmd.append("--auto-nets")
    if auto_hosts:
        cmd.append("--auto-hosts")
    if daemon:
        cmd.append("--daemon")

    for ex in excludes:
        if ex:
            cmd.extend(["-x", ex.strip()])

    cmd.extend([s.strip() for s in subnets if s.strip()])
    return cmd

def main():
    print("sshuttle CLI\n")

    remote = get_remote()
    subnets = get_subnets()
    excludes = get_excludes()
    dns = yes("Enable DNS tunneling?")
    auto_nets = yes("Enable auto-detection of remote subnets (--auto-nets)?")
    auto_hosts = yes("Enable auto-hosts update (--auto-hosts)?")
    daemon = yes("Run in daemon mode (--daemon)?")

    cmd = build_command(remote, subnets, excludes, dns, auto_nets, auto_hosts, daemon)

    print("\n[+] Executing command:")
    print(" ".join(cmd))
    print("\n[+] Output:\n")

    try:
        subprocess.run(cmd)
    except FileNotFoundError:
        print("'sshuttle' is not installed.")
    except Exception as e:
        print(f"Error running sshuttle: {e}")

if __name__ == "__main__":
    main()
