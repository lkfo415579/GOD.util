FAST_PATH=~/fast_align/b
echo "./run_fast.sh src tgt"
# prepare fast
~/GOD.util/moses-scripts/prepare-fast-align.perl $1 $2 > tmp2.enzh
# clean tmp.enzh
grep "^ |||" -n tmp2.enzh > error_lines
grep "||| $" -n tmp2.enzh >> error_lines
python ~/GOD.util/corpus-script/remove_line_num.py tmp2.enzh error_lines > tmp.enzh
# run fast align
$FAST_PATH/fast_align -i tmp.enzh -d -o -v > forward.align
$FAST_PATH/fast_align -i tmp.enzh -d -o -v -r > reverse.align
$FAST_PATH/atools -i forward.align -j reverse.align -c grow-diag-final-and > grow-diag-final-and
# clean
rm tmp.enzh forward.align reverse.align tmp2.enzh
