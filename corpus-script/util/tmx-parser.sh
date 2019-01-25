echo "usage: tmx-parser.sh lang file.tmx"
# grep -oP '"'$1'"><seg>\K(.*)<' $2 | sed 's/<\/seg><//g' > $1.txt
grep -o ">.*<" $1 |cut -f3 | sed 's/<$//g' > $2
