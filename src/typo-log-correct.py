#!/usr/bin/env python3
import sys
import sqlite3
from pathlib import Path
import shutil
import time

DB_PATH = Path.home() / ".local/share/typo-stats.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Commands table
    c.execute("""
    CREATE TABLE IF NOT EXISTS commands (
        name TEXT PRIMARY KEY,
        correct INTEGER DEFAULT 0,
        incorrect INTEGER DEFAULT 0,
        max_streak INTEGER DEFAULT 0,
        current_streak INTEGER DEFAULT 0
    )
    """)

    # Mistypes table
    c.execute("""
    CREATE TABLE IF NOT EXISTS mistypes (
        name TEXT PRIMARY KEY,
        count INTEGER DEFAULT 0
    )
    """)

    # Meta table
    c.execute("""
    CREATE TABLE IF NOT EXISTS meta (
        key TEXT PRIMARY KEY,
        value INTEGER
    )
    """)

    # Ensure meta keys exist
    for key in [
        "total_commands",
        "correct",
        "incorrect",
        "max_correct_streak",
        "current_correct_streak",
        "start_time"
    ]:
        c.execute("INSERT OR IGNORE INTO meta VALUES (?, ?)", (key, 0))

    # Set start_time if not already
    c.execute("SELECT value FROM meta WHERE key='start_time'")
    if c.fetchone()[0] == 0:
        c.execute("UPDATE meta SET value=? WHERE key='start_time'", (int(time.time()),))

    conn.commit()
    return conn

def main():
    if len(sys.argv) < 2:
        return

    command = sys.argv[1]

    # Only log real commands
    if not shutil.which(command):
        return

    conn = init_db()
    c = conn.cursor()

    # Update totals
    c.execute("UPDATE meta SET value = value + 1 WHERE key='total_commands'")
    c.execute("UPDATE meta SET value = value + 1 WHERE key='correct'")
    c.execute("UPDATE meta SET value = value + 1 WHERE key='current_correct_streak'")

    # Update per-command stats
    c.execute("""
    INSERT INTO commands(name, correct, incorrect, max_streak, current_streak)
    VALUES (?, 1, 0, 1, 1)
    ON CONFLICT(name) DO UPDATE SET
        correct = correct + 1,
        current_streak = current_streak + 1,
        max_streak = MAX(max_streak, current_streak)
    """, (command,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
