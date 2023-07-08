#!/bin/bash

# Directory to output rst files
startdir="/forensicVM/main/django-app/docs/build/htmlhelp"
outputdir="/forensicVM/main/django-app/docs/build/outputdir"

# Process each HTML file
while IFS= read -r -d '' file
do
    # Convert encoding to UTF-8 and save as new file
    iconv -f ISO-8859-1 -t UTF-8 "$file" > "${file%.html}_utf8.html"

    # Convert HTML to reStructuredText using Pandoc
    pandoc -s "${file%.html}_utf8.html" -o "${file%.html}.rst"

done < <(find "$startdir" -name '*.html' ! -name '*.html.*' -print0)

# Sync the resulting .rst files to the output directory, preserving directories structure
rsync -avm --include='*.rst' -f 'hide,! */' "$startdir" "$outputdir"
