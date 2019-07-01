F=$(find ./ -name "*en*" | sed 's/en/'$1'/g')
# echo $F
for i in $F
do
    en=$(echo $i |sed 's/'$1'/en/g')
    echo $en -> $i
    mv $en $i
done
