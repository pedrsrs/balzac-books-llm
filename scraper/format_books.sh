#!/bin/bash

folder_path="./books"
cd $folder_path

for file in *.txt; do
    
    if [ -e "$file" ]; then

        end_marker_line=$(awk '/\*\*\* END OF THE PROJECT GUTENBERG EBOOK/{print NR; exit}' "$file")

        if [ -n "$end_marker_line" ]; then
            head -n "$((end_marker_line - 1))" "$file" > "$file.tmp"
            mv "$file.tmp" "$file"

            file_title=$(basename "$file" | sed 's/\.txt$//')
            
            formatted_title=$(echo "$file_title" | tr '[:lower:]' '[:upper:]' | sed 's/_/ /g')
            echo $formatted_title
            last_occurrence_line=$(awk -v pattern="$formatted_title" 'BEGIN{IGNORECASE=1} {if ($0 ~ pattern) {pos=match($0, pattern); if (pos) lastpos=NR}} END{print lastpos}' "$file")
            echo $last_occurrence_line

            if [ -n "$last_occurrence_line" ]; then
                tail -n +"$last_occurrence_line" "$file" | sed 's/\.txt//' > "$file.tmp"
                mv "$file.tmp" "$file"
                echo "Processed: $file"
            else
                echo "Error: Unable to find the last occurrence of the formatted title in $file"
            fi

        else
            echo "Error: Unable to find the end marker in $file"
        fi
    else
        echo "Warning: $file does not exist"
    fi
done

echo "Script completed"
