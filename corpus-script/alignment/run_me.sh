echo "usage: align_file source target"
python find_err_align.py $1 3
python ~/GOD.util/corpus-script/remove_line_num.py \
$2 err "|||" 0 > error_lines.src
python ~/GOD.util/corpus-script/remove_line_num.py \
$3 err "|||" 0 > error_lines.tgt
