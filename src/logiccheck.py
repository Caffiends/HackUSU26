#!/bin/python3
import subprocess
import sys
import difflib
import shutil

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
    "lsusb",
    "echo",
    "ls"
]

def main():
    user_command = sys.argv[1]
    user_args = sys.argv[2:]

    match = difflib.get_close_matches(user_command, COMMON_COMMANDS, n=1, cutoff=0.6)

    if match:
        corrected = match[0]
        subprocess.run([f"typo-{corrected}", *user_args])
    else:
        print(f"{user_command}: command not found")

if __name__ == "__main__":
    main()
