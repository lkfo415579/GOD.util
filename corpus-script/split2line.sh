echo "usage: file lang1 lang2"
sed -n '0~2p' $1 > all.$3
sed -n '1~2p' $1 > all.$2
