#!/bin/bash

# Directory to search for binary files (update this path accordingly)
SEARCH_DIRECTORY="./forensicVM"

# Output file for debian/source/include-binaries
INCLUDE_BINARIES_FILE="debian/source/include-binaries"

# Find binary files and write to the include-binaries file
find "$SEARCH_DIRECTORY" -type f -exec file {} \; | grep -E ":.* (executable|shared object)" | awk -F: '{print $1}' > "$INCLUDE_BINARIES_FILE"

echo "Binary files found and added to $INCLUDE_BINARIES_FILE:"
cat "$INCLUDE_BINARIES_FILE"

