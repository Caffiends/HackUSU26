#!/bin/bash

# --- Configuration ---
PROJECT="shame"
REPO_URL="https://github.com/Caffiends/HackUSU26.git"
INSTALL_DIR="/usr/local/bin"
VENV_DIR="/opt/${PROJECT}-venv"

set -e

echo "🚀 Installing $PROJECT tools..."

# Ensure dependencies exist (Docker already uses apt)
apt-get update
apt-get install -y git python3 python3-venv python3-pip zsh
apt-get clean

# Create install directory
mkdir -p "$INSTALL_DIR"

# Clone repository
WORKDIR=$(mktemp -d)
git clone "$REPO_URL" "$WORKDIR"

# Copy source scripts
cp "$WORKDIR"/HackUSU26/src/* "$INSTALL_DIR"/

# Make scripts executable
chmod +x "$INSTALL_DIR"/typo-*
chmod +x "$INSTALL_DIR"/typo-wrapper
chmod +x "$INSTALL_DIR"/typo-stats
chmod +x "$INSTALL_DIR"/typo-log-correct

# Optional isolated venv (cleaner location)
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip

# Cleanup
rm -rf "$WORKDIR"

echo "✅ $PROJECT installed into $INSTALL_DIR"
