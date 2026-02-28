#!/bin/python3

import subprocess
import sys
import shutil
import difflib

# Common commands you want to allow autocorrect for
COMMON_COMMANDS = [
    "zip",
    "sudo",
    "mv",
    "cat",
    "ps",
    "rm",
    "mount",
    "dd",
    "nmap",
    "dig",
    "nslookup",
    "ipconfig",
    "whoami",
    "docker",
    "paste",
    "vim",
    "vi",
    "git",
    "clear",
    "ping",
    "man",
    "touch",
    "mkdir",
    "arp",
    "neofetch",
    "fastfetch",
    "grep",
    "iptables",
    "rmdir",
    "passwd",
    "traceroute",
    "curl",
    "wget",
    "kill",
    "pskill",
    "ps",
    "date",
    "time",
    "trap",
    "lsblk",
    "lspci",
    "lsusb"
]

def logic():
    if len(sys.argv) < 2:
        print("Usage: script.py <command> [args...]")
        sys.exit(1)

    user_command = sys.argv[1]
    user_args = sys.argv[2:]

    # If command exists normally, just run it
    if shutil.which(user_command):
        subprocess.run([user_command] + user_args)
        return

    # Try to find closest match
    match = difflib.get_close_matches(user_command, COMMON_COMMANDS, n=1, cutoff=0.6)
    print(match)

    if match:
        corrected = match[0]
        subprocess.run(['bash', f"typo-{corrected}"])
    else:
        print(f"Command '{user_command}' not found.")

if __name__ == '__main__':
    logic()
