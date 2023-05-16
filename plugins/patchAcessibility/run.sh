#!/bin/bash -

PLUGIN_NAME="Patch accessibility"
PLUGIN_DESCRIPTION="If the forensic investigator presses shit five times, it gets a command shell"
OS_NAME="windows"
OS_VERSION=("xp" "7" "8" "8.1" "10" "11")
AUTHOR="Nuno Mourinho"
VERSION="1.0"
LICENSE="GPL"

function get_plugin_info() {
  # Build JSON object
  json="{"
  json+="\"plugin_name\":\"$PLUGIN_NAME\","
  json+="\"plugin_description\":\"$PLUGIN_DESCRIPTION\","
  json+="\"os_name\":\"$OS_NAME\","
  json+="\"os_version\":\"$OS_VERSION\","
  json+="\"author\":\"$AUTHOR\","
  json+="\"version\":\"$VERSION\","
  json+="\"license\":\"$LICENSE\""
  json+="}"

  # Return JSON object

  echo $json
}


function run_plugin() {
set -e
/forensicVM/bin/remove-hibernation.sh $1
guestfile="$1"

guestfish --rw -i $guestfile <<'EOF'
   mv /Windows/System32/sethc.exe /Windows/System32/sethc.exe.bak
   cp /Windows/System32/cmd.exe /Windows/System32/sethc.exe
   exit
EOF
}


# Check the first parameter and call the appropriate function
if [[ "$1" == "run" ]]; then
  run_plugin $2
elif [[ "$1" == "info" ]]; then
  get_plugin_info
else
  echo "Invalid parameter. Usage: ./myscript.sh [run|info]"
  exit 1
fi



