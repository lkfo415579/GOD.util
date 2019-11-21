SRCL=en
TGTL=zh
SCRIPT=~/GOD.util/corpus-script
TERM=Medicine
FILTER=true
# clean double, 1 is space, 0 is char
CLEAN_DOUBLE=true
D1=1
D2=1
# normalize speical upper letter 2 lower letter
NORMAL=true
# is BPE tied together
MIX=false
echo "0. SRCL:"$SRCL" TGTL:"$TGTL
# 1
echo "1. duplicated clean"
$SCRIPT/dup.delete.pl all.$SRCL all.$TGTL
mv final_all.$SRCL all.$SRCL
mv final_all.$TGTL all.$TGTL
# 2
echo "2. remove non-utf8"
$SCRIPT/remove_utf8.sh all.$SRCL > f.$SRCL
$SCRIPT/remove_utf8.sh all.$TGTL > f.$TGTL
mv f.$SRCL all.$SRCL
mv f.$TGTL all.$TGTL
# 3
echo "3. remove mutiple lines"
python $SCRIPT/Remove_Line.py all.$SRCL
python $SCRIPT/Remove_Line.py all.$TGTL
mv all.$SRCL.without_external_line all.$SRCL
mv all.$TGTL.without_external_line all.$TGTL
# 4
# en-zh
if [ $FILTER == true ]
then
    echo "4. clean language pair err"
    python $SCRIPT/../python_toolkit/pair_lang_filter.py all $TGTL $SRCL all.filter
    mv all.filter.$SRCL all.$SRCL
    mv all.filter.$TGTL all.$TGTL
fi
# 5.1
if [ $NORMAL == true ]
then
    echo "5.1 normalizing symbols of target corpus"
    $SCRIPT/../util_token/normalize_symbols.perl < all.$TGTL > all.t.$TGTL
    $SCRIPT/../util_token/normalize_symbols.perl < all.$SRCL > all.t.$SRCL
    mv all.t.$TGTL all.$TGTL
    mv all.t.$SRCL all.$SRCL
fi

echo "5. util auto processing"
mv all.$SRCL all.en
mv all.$TGTL all.zh
if [ $SRCL == 'en' ] && [ $TGTL == 'zh' ]
then
    $SCRIPT/../util_token/auto-preprocessing/AUTO-pre-processing.sh all
elif [ $TGTL == 'de' ]
then
    $SCRIPT/../util_token/auto-preprocessing/AUTO-pre-processing-Both-EN-tok.sh all
elif [ $SRCL != 'en' ]
then
    echo "No-EN-Tok"
    $SCRIPT/../util_token/auto-preprocessing/AUTO-pre-processing-No-EN-tok.sh all
else
    $SCRIPT/../util_token/auto-preprocessing/AUTO-pre-processing-No-ZH-tok.sh all
fi
#
# chinese
if  [ $CLEAN_DOUBLE == true ]
then
    echo "6. clean double length sents"
    python $SCRIPT/clean_double_len.py all.en-zh.clean.en all.en-zh.clean.zh 3.0 $D1 $D2
    python $SCRIPT/clean_double_len.py all.zh-en.clean.en all.zh-en.clean.zh 3.0 $D1 $D2

    mv all.en-zh.clean.en.double all.en-zh.clean.en
    mv all.en-zh.clean.zh.double all.en-zh.clean.zh
    mv all.zh-en.clean.en.double all.zh-en.clean.en
    mv all.zh-en.clean.zh.double all.zh-en.clean.zh
fi
# 7
echo "7. BPE"
mv all.en-zh.clean.en corpus.$SRCL-$TGTL.$SRCL
mv all.en-zh.clean.zh corpus.$SRCL-$TGTL.$TGTL
mv all.zh-en.clean.en corpus.$TGTL-$SRCL.$SRCL
mv all.zh-en.clean.zh corpus.$TGTL-$SRCL.$TGTL
#-- bpe procedure
mkdir -p $SRCL-$TGTL $TGTL-$SRCL
mv corpus.$SRCL-$TGTL.* $SRCL-$TGTL/
mv corpus.$TGTL-$SRCL.* $TGTL-$SRCL/
# en-zh
if [ $MIX == true ]
then
    BPE=$SCRIPT/../BPE_TOOLKIT/pre_mix.sh
else
    BPE=$SCRIPT/../BPE_TOOLKIT/pre.sh
fi
cp $BPE ./pre.sh
sed -i "s/SRCL=.*$/SRCL="$SRCL"/g" pre.sh
sed -i "s/TGTL=.*$/TGTL="$TGTL"/g" pre.sh
sed -i "s/P=.*$/P="corpus.$SRCL-$TGTL"/g" pre.sh
sed -i "s/TERM=.*$/TERM="$TERM"/g" pre.sh
mv pre.sh $SRCL-$TGTL/
# zh-en
cp $SCRIPT/../BPE_TOOLKIT/pre.sh ./
sed -i "s/SRCL=.*$/SRCL="$TGTL"/g" pre.sh
sed -i "s/TGTL=.*$/TGTL="$SRCL"/g" pre.sh
sed -i "s/P=.*$/P="corpus.$TGTL-$SRCL"/g" pre.sh
sed -i "s/TERM=.*$/TERM="$TERM"/g" pre.sh
mv pre.sh $TGTL-$SRCL/
# run BPE
# remove previous data
cd $SRCL-$TGTL && ./pre.sh &
P1=$!
cd $TGTL-$SRCL && ./pre.sh &
P2=$!
wait $P1 $P2
cd $TGTL-$SRCL && rm corpus.$TGTL-$SRCL.*
cd ../
cd $SRCL-$TGTL && rm corpus.$SRCL-$TGTL.*
echo "script is done!"
