#!/bin/python3

import sys
import subprocess
import difflib
import shutil
import sqlite3
import time
from pathlib import Path

# ------------------------
# Configuration
# ------------------------

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

DB_PATH = Path.home() / ".local/share/typo-stats.db"

# ------------------------
# Database Setup
# ------------------------

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS meta (
        key TEXT PRIMARY KEY,
        value INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS commands (
        name TEXT PRIMARY KEY,
        correct INTEGER DEFAULT 0,
        incorrect INTEGER DEFAULT 0,
        max_streak INTEGER DEFAULT 0,
        current_streak INTEGER DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS mistypes (
        name TEXT PRIMARY KEY,
        count INTEGER DEFAULT 0
    )
    """)

    # Initialize meta values if missing
    for key in [
        "total_commands",
        "correct",
        "incorrect",
        "max_correct_streak",
        "current_correct_streak",
        "start_time"
    ]:
        c.execute("INSERT OR IGNORE INTO meta VALUES (?, ?)", (key, 0))

    # Ensure start_time is set
    c.execute("SELECT value FROM meta WHERE key='start_time'")
    if c.fetchone()[0] == 0:
        c.execute("UPDATE meta SET value=? WHERE key='start_time'", (int(time.time()),))

    conn.commit()
    return conn

# ------------------------
# Logging Logic
# ------------------------

def log_command(conn, command, correct):
    c = conn.cursor()

    # Update totals
    c.execute("UPDATE meta SET value = value + 1 WHERE key='total_commands'")

    if correct:
        c.execute("UPDATE meta SET value = value + 1 WHERE key='correct'")
        c.execute("UPDATE meta SET value = value + 1 WHERE key='current_correct_streak'")

        # Update max streak
        c.execute("SELECT value FROM meta WHERE key='current_correct_streak'")
        current = c.fetchone()[0]

        c.execute("SELECT value FROM meta WHERE key='max_correct_streak'")
        max_streak = c.fetchone()[0]

        if current > max_streak:
            c.execute("UPDATE meta SET value=? WHERE key='max_correct_streak'", (current,))

        # Update per-command stats
        c.execute("""
        INSERT INTO commands(name, correct, incorrect, max_streak, current_streak)
        VALUES (?, 1, 0, 1, 1)
        ON CONFLICT(name) DO UPDATE SET
            correct = correct + 1,
            current_streak = current_streak + 1,
            max_streak = MAX(max_streak, current_streak + 1)
        """, (command,))

    else:
        c.execute("UPDATE meta SET value = value + 1 WHERE key='incorrect'")
        c.execute("UPDATE meta SET value = 0 WHERE key='current_correct_streak'")

        c.execute("""
        INSERT INTO mistypes(name, count)
        VALUES (?, 1)
        ON CONFLICT(name) DO UPDATE SET
            count = count + 1
        """, (command,))

    conn.commit()

# ------------------------
# Command Execution Logic
# ------------------------

def run_real_command(command, args):
    full_path = shutil.which(command)
    if full_path:
        subprocess.run([full_path] + args)
        return True
    return False


def main():
    if len(sys.argv) < 2:
        sys.exit(0)

    user_command = sys.argv[1]
    user_args = sys.argv[2:]

    conn = init_db()

    # If real command exists → run normally
    if shutil.which(user_command):
        log_command(conn, user_command, True)
        subprocess.run([user_command] + user_args)
        conn.close()
        return

    # Try fuzzy match
    match = difflib.get_close_matches(user_command, COMMON_COMMANDS, n=1, cutoff=0.6)

    if match:
        corrected = match[0]
        prank_script = shutil.which(f"typo-{corrected}")

        # Log incorrect attempt
        log_command(conn, user_command, False)

        if prank_script:
            subprocess.run([prank_script] + user_args)
        else:
            # fallback to real command
            run_real_command(corrected, user_args)

    else:
        log_command(conn, user_command, False)
        print(f"{user_command}: command not found")

    conn.close()


if __name__ == "__main__":
    main()
