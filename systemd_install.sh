
#!/bin/bash

# Configures the system so that it starts setup_ir.sh as root, followed by
# main.py as non-root user.
# Because it changes the system configuration, the script itself must be run as
# root.

set -eu

usage() {
    echo "Usage: $0 <username>"
    exit 1
}

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Error: This script must be run as root."
    exit 1
fi

# Check if an argument is provided
if [ $# -ne 1 ]; then
    echo "Error: No username provided."
    usage
fi

USERNAME="$1"

# Check if the user exists
if ! id "$USERNAME" > /dev/null; then
    echo "Error: User '$USERNAME' does not exist."
    exit 2
fi

# Check if the user is root
USER_ID=$(id -u "$USERNAME")
if [ "$USER_ID" -eq 0 ]; then
    echo "Error: '$USERNAME' is the root user. Please provide a non-root user."
    exit 3
fi

SCRIPT_DIR="$(realpath "$(dirname "$0")")"

# Check if .venv directory exists and contains a valid virtual environment
if [ ! -d "$SCRIPT_DIR/.venv" ] || [ ! -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    echo "Error: The .venv directory does not exist or is not a valid virtual environment."
    exit 4
fi

# Disable the two services, thus clearing any existing symlinks.
systemctl disable irsetup.service speakerir.service || true

# Generate the two services' units on the fly

cat <<EOF > /lib/systemd/system/irsetup.service
[Unit]
Description=SpeakerIR Remote Control Setup
After=basic.target
After=network-online.target

[Service]
Type=oneshot
ExecStart=${SCRIPT_DIR}/setup_ir.sh
WorkingDirectory=${SCRIPT_DIR}

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > /lib/systemd/system/speakerir.service
[Unit]
Description=SpeakerIR main application
After=basic.target
Requires=irsetup.service
After=irsetup.service

[Service]
Type=exec
ExecStart=${SCRIPT_DIR}/.venv/bin/python3 main.py
WorkingDirectory=${SCRIPT_DIR}
User=${USERNAME}
Group=${USERNAME}

[Install]
WantedBy=multi-user.target
EOF

systemctl enable irsetup.service speakerir.service
systemctl daemon-reload