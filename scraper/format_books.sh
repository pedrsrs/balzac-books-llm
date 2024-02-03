#!/bin/bash

directory="./books/"

for file in "$directory"*.txt; do
    if [ -f "$file" ]; then
        marker="*** END OF THE PROJECT GUTENBERG EBOOK"
        temp_file="${file%.txt}_temp.txt"

        awk -v marker="$marker" '{print} $0 ~ marker{exit}' "$file" > "$temp_file"

        mv "$temp_file" "$file"

        echo "Processed: $file"
    fi
done

echo "Processing complete."
