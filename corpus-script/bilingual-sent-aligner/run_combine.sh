S_F=$(find *-s*)
mkdir -p com/
for f in $S_F
do
    # echo $f
    f2=$(echo $f | sed 's/-s/-t/g')
    output=$(echo $f | cut -d '.' -f1 | sed 's/-s//g').bitext
    # echo $output
    ./prepare-fast-align.perl $f $f2 > com/$output
done
