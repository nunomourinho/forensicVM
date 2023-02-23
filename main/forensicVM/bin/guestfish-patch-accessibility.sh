#!/bin/bash -
set -e
guestfile="$1"

guestfish --rw -i $guestfile <<'EOF'
   mv /Windows/System32/sethc.exe /Windows/System32/sethc.exe.bak
   cp /Windows/System32/cmd.exe /Windows/System32/sethc.exe
   exit
EOF
