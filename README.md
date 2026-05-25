# Auto Git Streak Bot

An automated Python script that logs timestamps and pushes them to GitHub on a schedule using `systemd`. 

## Quick Start (For Others)

1. **Download the project** into your desired directory.
2. **Run the script once manually** to configure your credentials:
   ```bash
   python3 auto_git.py
   ```
   *(It will prompt for your username, GitHub Personal Access Token, and repo URL, then create a secure `config.ini` file automatically).*

3. **Install the background service** using the instant installation command below.

## Features
* **Interactive First-Time Setup**: Prompts for credentials if missing, then runs hands-free forever.
* **Auto-Secured**: Automatically locks file permissions on `config.ini` so other local users can't read your token.
* **Force Push Enabled**: Bypasses merge rejections smoothly to ensure consistency.

## Instant Systemd Installation

Run this single command block inside the project directory to automatically generate, enable, and start the 10-minute automated background timer:

```bash
sudo tee /etc/systemd/system/holy_comments.service <<EOF
[Unit]
Description=Automated Holy Comments Git Bot
After=network.target

[Service]
Type=oneshot
User=\$USER
WorkingDirectory=\$PWD
ExecStart=/usr/bin/python3 \$PWD/auto_git.py
EOF

sudo tee /etc/systemd/system/holy_comments.timer <<EOF
[Unit]
Description=Run Holy Comments Script Every 10 Minutes

[Timer]
OnBootSec=2min
OnUnitActiveSec=10min

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload && sudo systemctl enable --now holy_comments.timer
```
