echo "usage: tmx-parser.sh lang file.tmx"
# grep -oP '"'$1'"><seg>\K(.*)<' $2 | sed 's/<\/seg><//g' > $1.txt
# grep -o ">.*<" $1 |cut -f3 | sed 's/<$//g' > $2
grep -o "seg>.*<\/" $1 | sed 's/^seg>//' | sed 's/<\/seg><\///' > $1.out

sed -n '0~2p' $1.out > $1.1
sed -n '1~2p' $1.out > $1.2
