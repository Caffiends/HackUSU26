#!/bin/bash

# --- Configuration ---
PROJECT="dropship"
REPO_URL="https://raw.githubusercontent.com/Caffiends/HackUSU26/refs/heads/main/"
INSTALL_DIR="/opt/$PROJECT"
VENV_DIR="$INSTALL_DIR/venv"
BACKUP_DIR="$HOME/.${PROJECT}_backups"

# Check for root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Please run as root, peasant"
   exit 1
fi

echo "Uninstalling $PROJECT... wimp"

# Remove binaries

