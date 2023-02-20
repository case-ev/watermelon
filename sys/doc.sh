#!/bin/bash

# This script compiles all the documentation to HTML. It is not necessary, since
# the documentation is readable as a Markdown file.

mkdir build/docs/temp -p
cd docs

BUILD_DIR="../build/docs"
target="html"
FILES=(
    examples.md
    graph.md
    vertices.md
    agents.md
    soc.md
)

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
        title=${title#\# }
        cat "$file" | tail -n +2 > "${BUILD_DIR}/temp/${filename}.md"
        pandoc -f markdown -t $target "${BUILD_DIR}/temp/${filename}.md" -o "${BUILD_DIR}/${filename}.${target}" --lua-filter lua/link_files.lua --metadata title="$title" --template pandoc-toc-sidebar/toc-sidebar.html --toc -B template/nav
    fi
done

echo -e "Compiling \x1b[32;20mall files\x1b[0m"
pandoc -f markdown -t $target ${FILES[@]} -o "${BUILD_DIR}/all.${target}" --lua-filter lua/link_files.lua --embed-resources --standalone --metadata title="Watermelon - docs" --template pandoc-toc-sidebar/toc-sidebar.html --toc -B template/nav

echo -e "Cleaning up"
rm -rf "${BUILD_DIR}/temp/"

echo -e "\x1b[32;20mSuccesfully built documentation\x1b[0m"
