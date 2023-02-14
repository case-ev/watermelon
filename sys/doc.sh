#!/bin/bash


mkdir build/doc/temp -p
cd doc

BUILD_DIR="../build/doc"

for file in *; do
    if [ -f "$file" ]; then
        echo -e "Compiling doc file \x1b[32;20m${file}\x1b[0m"
        filename="${file%.md}"
        title=`cat "$file" | head -n 1`
        cat "$file" | tail -n +2 > "${BUILD_DIR}/temp/${filename}.md"
        pandoc -f markdown -t html "${BUILD_DIR}/temp/${filename}.md" -o "${BUILD_DIR}/${filename}.html" --css=styles/main.css --embed-resources --standalone --metadata title="$title"
    fi
done
