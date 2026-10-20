#!/bin/bash
# Run from the repo root
# exit codes: 0=ok, 2=usage, 3=compile, 4=upload

error=$(tput setaf 1)
success=$(tput setaf 2)
reset=$(tput sgr0)

PORT="$1"

if [ -z "$PORT" ]
then
    echo "usage: ./flash.sh <PORT>"
    exit 2
fi

echo "[*] compiling..."

if ! arduino-cli compile --fqbn arduino:avr:uno --build-path build/arduino arduino/servo_led ; then
    echo "${error}compile failed${reset}"
    exit 3
fi

echo "[*] ${success}compile complete${reset}"
echo "[*] uploading to $PORT"

if ! arduino-cli upload -p "$PORT" --fqbn arduino:avr:uno arduino/servo_led ; then
    echo "${error}upload failed${reset}"
    exit 4
fi

echo "[*] ${success}uploading complete${reset}"

exit 0