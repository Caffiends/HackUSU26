#!/bin/bash

# --- Configuration ---
PROJECT="shame"
INSTALL_DIR="/usr/local/bin/$PROJECT"
VENV_DIR="$INSTALL_DIR/venv"
BACKUP_DIR="$HOME/.${PROJECT}_backups"

# Check for root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Please run as root, peasant"
   exit 1
fi

echo "Uninstalling $PROJECT... wimp"

# Revert rc Files
rm -rf "$HOME/.zshrc"
[[ -f "$BACKUP_DIR/.bashrc.bak" ]] && cp "$BACKUP_DIR/.bashrc.bak" "$HOME/.bashrc"
[[ -f "$BACKUP_DIR/.zshrc.bak" ]] && cp "$BACKUP_DIR/.zshrc.bak" "$HOME/.zshrc"

# Remove Files
rm -rf "$INSTALL_DIR"
