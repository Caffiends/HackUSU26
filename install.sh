#!/bin/bash

# --- Configuration ---
PROJECT="shame"
REPO_URL="https://github.com/Caffiends/HackUSU26.git"
INSTALL_DIR="/usr/local/bin"
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

# 3. Download Source Code
git clone "$REPO_URL"
cp ./HackUSU26/src/* "$INSTALL_DIR/."
chmod +x "$INSTALL_DIR/typo-*"

# 4. Isolated Python Environment
echo "🐍 Setting up Python terminal surveillance... (the poor-man's keylogger)"
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip
# If you have a requirements.txt, run: "$VENV_DIR/bin/pip" install -r requirements.txt

# 5. Respectful Migration of Existing Shell Setup
echo "Migrating aliases and PATH from .bashrc..."
if [[ -f "$HOME/.bashrc" ]]; then
    {
        echo -e "\n# --- Migrated by $PROJECT ---"
        grep -E "^(alias|export|PATH)" "$HOME/.bashrc" | grep -v "PS1"
    } >> "$HOME/.zshrc"
fi

# 6. Zsh Setup
cat ./HackUSU26/append.zsh >> ~/.zshrc

# 7. Finalize
rm -rf ./HackUSU26

chsh -s "$(which zsh)" "$whoami"
echo "✅ $PROJECT successfully installed. Your commands will be logged locally and will not leave your machine."
echo "Your SH-ame is your own."

# 8. Restart Shell
echo "Activating... good luck lol."
exec zsh
