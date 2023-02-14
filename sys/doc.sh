#!/bin/bash

# This script compiles all the documentation to HTML. It is not necessary, since
# the documentation is readable as a Markdown file.

mkdir build/doc/temp -p
cd doc

BUILD_DIR="../build/doc"
target="html"

while getopts "hpT:" arg
do
    case "$arg" in
        h)
            target="html"
            ;;
        p)
            target="pdf"
            ;;
        T)
            target="${OPTARG}"
            ;;
    esac
done

for file in *; do
    if [ -f "$file" ]; then
        echo -e "Compiling doc file \x1b[32;20m${file}\x1b[0m"
        filename="${file%.md}"
        title=`cat "$file" | head -n 1`
        cat "$file" | tail -n +2 > "${BUILD_DIR}/temp/${filename}.md"
        pandoc -f markdown -t $target "${BUILD_DIR}/temp/${filename}.md" -o "${BUILD_DIR}/${filename}.${target}" --css=styles/main.css --embed-resources --standalone --metadata title="$title"
    fi
done

echo -e "Removing temp directory"
rm -rf "${BUILD_DIR}/temp/"
