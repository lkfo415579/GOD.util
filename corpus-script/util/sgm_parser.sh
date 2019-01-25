grep -o ">.*<" $1 | sed 's/^>//g' | sed 's/<$//g'
