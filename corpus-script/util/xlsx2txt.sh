ls *.xlsx | xargs -I {} ssconvert -O 'separator="|||" format=raw' {} {}.txt
