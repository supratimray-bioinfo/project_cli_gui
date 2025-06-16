#!/bin/bash

echo "==================================="
echo "     Interactive Software Setup     "
echo "==================================="

# Function to get confirmation
confirm() {
    while true; do
        read -rp "$1 [y/n]: " yn
        case $yn in
            [Yy]*) return 0 ;;
            [Nn]*) return 1 ;;
            *) echo "Please answer yes or no." ;;
        esac
    done
}

# Detect Distro
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
    else
        echo "Could not detect distribution."
        exit 1
    fi
}

# -------------------
# Debian/Ubuntu setup
# -------------------
install_chrome_debian() {
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb
    sudo apt install -y /tmp/chrome.deb
    rm /tmp/chrome.deb
}

install_brave_debian() {
    sudo apt install -y curl
    sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave.com/signing-key.gpg
    echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | \
    sudo tee /etc/apt/sources.list.d/brave-browser-release.list > /dev/null
    sudo apt update
    sudo apt install -y brave-browser
}

# -------------------
# Fedora/Red Hat setup
# -------------------
install_chrome_fedora() {
    sudo dnf install -y https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
}

install_brave_fedora() {
    sudo dnf install -y dnf-plugins-core
    sudo dnf config-manager --add-repo https://brave-browser-rpm-release.s3.brave.com/x86_64/
    sudo rpm --import https://brave-browser-rpm-release.s3.brave.com/brave-core.asc
    sudo dnf install -y brave-browser
}

# Update system
update_system() {
    case $DISTRO in
        ubuntu|debian)
            sudo apt update && sudo apt upgrade -y ;;
        fedora)
            sudo dnf upgrade --refresh -y ;;
        *)
            echo "System update not supported for $DISTRO" ;;
    esac
}

# Run
detect_distro
echo "Detected distribution: $DISTRO"

if confirm "Do you want to update your system?"; then
    update_system
fi

if confirm "Do you want to install Google Chrome?"; then
    case $DISTRO in
        ubuntu|debian)
            install_chrome_debian ;;
        fedora)
            install_chrome_fedora ;;
        *)
            echo "Chrome installation not supported on $DISTRO." ;;
    esac
fi

if confirm "Do you want to install Brave Browser?"; then
    case $DISTRO in
        ubuntu|debian)
            install_brave_debian ;;
        fedora)
            install_brave_fedora ;;
        *)
            echo "Brave installation not supported on $DISTRO." ;;
    esac
fi

echo "==================================="
echo "      Installation Completed       "
echo "==================================="
