#!/bin/bash

cd ./books

main() {
    for file in *.txt; do
        if [ -e "$file" ]; then
            format_end_of_book "$file"
            format_addendum "$file"
        else
            echo "Warning: $file does not exist"
        fi
    done

    concatenate_files
}

format_addendum() {
    file="$1"

    addendum_line=$(awk -v pattern="ADDENDUM" 'BEGIN{IGNORECASE=1} {if ($0 ~ pattern) {pos=match($0, pattern); if (pos) lastpos=NR}} END{print lastpos}' "$file")
    
    if [ -n "$addendum_line" ]; then
        head -n "$((addendum_line - 1))" "$file" > "$file.tmp"
        mv "$file.tmp" "$file"
    fi
}

format_beggining_of_book() {
    file="$1"

    file_title=$(basename "$file" | sed 's/\.txt$//')
            
    formatted_title=$(echo "$file_title" | tr '[:lower:]' '[:upper:]' | sed 's/_/ /g')
    last_occurrence_line=$(awk -v pattern="$formatted_title" 'BEGIN{IGNORECASE=1} {if ($0 ~ pattern) {pos=match($0, pattern); if (pos) lastpos=NR}} END{print lastpos}' "$file")

    if [ -n "$last_occurrence_line" ]; then
        tail -n +"$last_occurrence_line" "$file" > "$file.tmp"
        mv "$file.tmp" "$file"
    fi
}

format_end_of_book() {
    file="$1"

    end_marker_line=$(awk '/\*\*\* END OF THE PROJECT GUTENBERG EBOOK/{print NR; exit}' "$file")

    if [ -n "$end_marker_line" ]; then
        head -n "$((end_marker_line - 1))" "$file" > "$file.tmp"
        mv "$file.tmp" "$file"
    fi
}

concatenate_files() {
    cat *.txt > ../balzac_full_books.txt
}

main
