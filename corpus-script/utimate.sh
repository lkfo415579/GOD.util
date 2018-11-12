SRCL=es
TGTL=zh
SCRIPT=~/GOD.util/corpus-script
TERM=Common
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
echo "4. clean double length sents"
# chinese
python $SCRIPT/clean_double_len.py all.$SRCL all.$TGTL 3.0 1 0
# en-es
# python $SCRIPT/clean_double_len.py all.$SRCL all.$TGTL 3.0 1 1
mv all.$SRCL.clean all.$SRCL
mv all.$TGTL.clean all.$TGTL
# 5
echo "5. clean language pair err"
# en-zh
python $SCRIPT/../python_toolkit/pair_lang_filter.py all zh en all.filter
mv all.filter.$SRCL all.$SRCL
mv all.filter.$TGTL all.$TGTL
# 6
echo "6. util auto processing"
mv all.$SRCL all.en
mv all.$TGTL all.zh
$SCRIPT/../util_token/auto-preprocessing/AUTO-pre-processing.sh all
# 7
echo "7. BPE"
mv all.en-zh.clean.en corpus.$SRCL-$TGTL.$SRCL
mv all.en-zh.clean.zh corpus.$SRCL-$TGTL.$TGTL
mv all.zh-en.clean.en corpus.$TGTL-$SRCL.$SRCL
mv all.zh-en.clean.zh corpus.$TGTL-$SRCL.$TGTL
#-- bpe procedure
# mkdir data
# mv * data
mkdir -p $SRCL-$TGTL $TGTL-$SRCL
mv corpus.$SRCL-$TGTL.* $SRCL-$TGTL/
mv corpus.$TGTL-$SRCL.* $TGTL-$SRCL/
# en-zh
cp $SCRIPT/../BPE_TOOLKIT/pre.sh ./
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
cd ../
cd $TGTL-$SRCL && ./pre.sh &
P2=$!
wait $P1 $P2
cd $TGTL-$SRCL && rm corpus.$TGTL-$SRCL.*
cd ../
cd $SRCL-$TGTL && rm corpus.$SRCL-$TGTL.*
echo "script is done!"
