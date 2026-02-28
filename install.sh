#!/bin/bash

# --- Configuration ---
PROJECT="dropship"
REPO_URL="https://raw.githubusercontent.com/Caffiends/HackUSU26/refs/heads/main/"
INSTALL_DIR="/usr/local/bin/$PROJECT"
VENV_DIR="$INSTALL_DIR/venv"
BACKUP_DIR="$HOME/.${PROJECT}_backups"

# Check for Root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Please run as root, peasant"
   exit 1
fi

echo "🚀 Starting $PROJECT Universal Installation..."

# 1. Detect Package Manager and Install Dependencies
install_pkg() {
    if command -v apt-get &>/dev/null; then
        apt-get update && apt-get install -y zsh python3-venv python3-pip
    elif command -v dnf &>/dev/null; then
        dnf install -y zsh python3 python3-pip
    elif command -v pacman &>/dev/null; then
        pacman -Syu --noconfirm zsh python python-pip
    elif command -v zypper &>/dev/null; then
        zypper install -y zsh python3 python3-pip
    else
        echo "❌ No supported package manager found (apt, dnf, pacman, zypper). WTF?"
        exit 1
    fi
}

install_pkg

# 2. Setup Filesystem & .rc Backups
mkdir -p "$INSTALL_DIR" "$BACKUP_DIR"
[[ -f "$HOME/.bashrc" ]] && cp "$HOME/.bashrc" "$BACKUP_DIR/.bashrc.bak"
[[ -f "$HOME/.zshrc" ]] && cp "$HOME/.zshrc" "$BACKUP_DIR/.zshrc.bak"

# 3. Install Binaries


# 4. Isolated Python Environment
echo "🐍 Setting up Python terminal surveillance... (the poor-man's keylogger)"
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip
# If you have a requirements.txt, run: "$VENV_DIR/bin/pip" install -r requirements.txt

# 5. Global Zsh Hook Setup
ZSHRC="/etc/zsh/zshrc"
HOOKS_FILE="hooks.zsh"

if ! curl -fsSL "$REPO_URL/$HOOKS_FILE" -o "$INSTALL_DIR/$HOOKS_FILE"; then
    "Could not retrieve hooks file, please check the repo URL or your internet connection."
    exit 1
fi

# Ensure global zshrc sources hooks (idempotent check)
if ! grep -q "$INSTALL_DIR/$HOOKS_FILE" "$ZSHRC_GLOBAL" 2>/dev/null; then
    echo "[ -f $INSTALL_DIR/$HOOKS_FILE ] && source $INSTALL_DIR/$HOOKS_FILE" >> "$ZSHRC_GLOBAL"
fi

# 6. Respectful Migration of Existing Shell Setup
echo "Migrating aliases and PATH from .bashrc..."
if [[ -f "$HOME/.bashrc" ]]; then
    {
        echo -e "\n# --- Migrated by $PROJECT ---"
        grep -E "^(alias|export|PATH)" "$HOME/.bashrc" | grep -v "PS1"
    } >> "$HOME/.zshrc"
fi

# 7. Finalize
chsh -s "$(which zsh)" "$SUDO_USER"
echo "✅ $PROJECT successfully installed. Your commands will be logged locally and will not leave your machine."
echo "Your shame is your own."

# 8. Restart Shell
echo "Activating... good luck lol."
exec zsh
