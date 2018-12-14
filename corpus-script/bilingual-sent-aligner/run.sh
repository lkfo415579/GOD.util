mkdir -p data/workshop
rm -r data/workshop/*
files=$(find data/*-s* -maxdepth 0)

for f in $files
do
    echo $f
    f2=${f##*/}
    python ~/GOD.util/util_token/detokenize.py -l zh < $f > data/workshop/tmp
    python -m jieba -d < data/workshop/tmp > data/workshop/$f2.tok
done

files=$(find data/*-t* -maxdepth 0)

for f in $files
do
    echo $f
    f2=${f##*/}
    cp $f data/workshop/$f2.tok
done


files=$(find data/workshop/*-s*)

for f in $files
do
    f2=$(echo $f | sed 's/\-s/\-t/g')
    echo $f
    echo $f2
    perl ./align-sents-all.pl $f2 $f 0.7
    python ~/GOD.util/util_token/detokenize.py -l zh < $f.aligned \
        | sed 's/  / /g' | sed 's/  / /g' > $f.res
    cp $f2.aligned $f2.res
done
