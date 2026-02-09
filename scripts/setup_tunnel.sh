#!/bin/bash
# Konfiguracja tunelu dla Node 3 (Piotrek)
# Hasło sudo: Legion303

echo "Configuring route for Node 3 (172.30.15.0/24)..."
echo "Legion303" | sudo -S ip ro add 172.30.15.0/24 via 192.168.18.10 2>/dev/null || echo "Route already exists or failed."
echo "Done."
