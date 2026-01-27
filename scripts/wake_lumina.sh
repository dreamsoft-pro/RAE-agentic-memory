#!/bin/bash
# Procedura zarządzania Lumina (Node 1) via VAIO (Tailscale)
# Hasło vaio: mwzmjsunp
# Hasło operator (root): (2ITj|xB.?%1~CeA>dCT{RJ`6rM2Q{E9WwjR9%lk

ACTION=${1:-wake}

if [ "$ACTION" == "stop" ]; then
    echo "Shutting down Lumina..."
    # Używamy vaio, aby wysłać polecenie lumina_stop (jeśli tam jest alias) 
    # lub bezpośrednio wyłączamy Luminę przez SSH jeśli jest dostępna
    sshpass -p "mwzmjsunp" ssh -o StrictHostKeyChecking=no vaio@100.78.171.96 "lumina_stop"
    echo "Shutdown command sent."
else
    echo "Connecting to VAIO to wake Lumina..."
    sshpass -p "mwzmjsunp" ssh -o StrictHostKeyChecking=no vaio@100.78.171.96 "echo 1 | lumina"
fi