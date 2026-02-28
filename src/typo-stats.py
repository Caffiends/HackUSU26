#!/usr/bin/env python3

import sqlite3
import time
from pathlib import Path
from datetime import timedelta

DB_PATH = Path.home() / ".local/share/typo-stats.db"

def get_meta(cursor, key):
    cursor.execute("SELECT value FROM meta WHERE key=?", (key,))
    row = cursor.fetchone()
    return row[0] if row else 0

def format_uptime(seconds):
    return str(timedelta(seconds=seconds))

def main():
    if not DB_PATH.exists():
        print("No stats database found.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    total = get_meta(c, "total_commands")
    correct = get_meta(c, "correct")
    incorrect = get_meta(c, "incorrect")
    max_streak = get_meta(c, "max_correct_streak")
    current_streak = get_meta(c, "current_correct_streak")
    start_time = get_meta(c, "start_time")

    uptime = int(time.time() - start_time) if start_time else 0
    accuracy = (correct / total * 100) if total else 0

    print("========== TYPO STATS ==========")
    print(f"Total Commands:        {total}")
    print(f"Correct:               {correct}")
    print(f"Incorrect:             {incorrect}")
    print(f"Accuracy:              {accuracy:.2f}%")
    print(f"Max Correct Streak:    {max_streak}")
    print(f"Current Streak:        {current_streak}")
    print(f"Uptime:                {format_uptime(uptime)}")
    print()

    # Top commands
    print("Top Commands:")
    c.execute("""
        SELECT name, correct
        FROM commands
        ORDER BY correct DESC
        LIMIT 5
    """)
    rows = c.fetchall()
    for name, count in rows:
        print(f"  {name:15} {count}")

    print()

    # Top mistypes
    print("Top Mistyped Commands:")
    c.execute("""
        SELECT name, count
        FROM mistypes
        ORDER BY count DESC
        LIMIT 5
    """)
    rows = c.fetchall()
    for name, count in rows:
        print(f"  {name:15} {count}")

    print()

    # Least mistyped
    c.execute("""
        SELECT name, count
        FROM mistypes
        ORDER BY count ASC
        LIMIT 1
    """)
    row = c.fetchone()
    if row:
        print(f"Least Mistyped Command: {row[0]} ({row[1]} times)")
    else:
        print("Least Mistyped Command: None")

    print()

    # Per-command ratios
    print("Per-Command Accuracy:")
    c.execute("""
        SELECT name, correct, incorrect
        FROM commands
        ORDER BY correct DESC
    """)
    rows = c.fetchall()
    for name, corr, inc in rows:
        total_cmd = corr + inc
        ratio = (corr / total_cmd * 100) if total_cmd else 0
        print(f"  {name:15} {ratio:6.2f}%  (C:{corr} / I:{inc})")

    conn.close()
    print("================================")

if __name__ == "__main__":
    main()
