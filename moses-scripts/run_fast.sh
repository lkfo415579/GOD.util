FAST_PATH=~/fast_align/build

# prepare fast
~/mosesdecoder/scripts/ems/support/prepare-fast-align.perl $1 $2 > tmp.enzh
# clean tmp.enzh
grep "^ |||" -n tmp.enzh > error_lines
grep "||| $" -n tmp.enzh >> error_lines
python ~/GOD.util/corpus_script/remove_line_num.py tmp.enzh error_lines > tmp.enzh
# run fast align
$FAST_PATH/fast_align -i tmp.enzh -d -o -v > forward.align
$FAST_PATH/fast_align -i tmp.enzh -d -o -v -r > reverse.align
$FAST_PATH/atools -i forward.align -j reverse.align -c grow-diag-final-and > grow-diag-final-and
# clean
rm tmp.enzh forward.align reverse.align
