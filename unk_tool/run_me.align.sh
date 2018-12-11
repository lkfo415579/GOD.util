echo "usage: ./run_me.align.sh test.bpe.en test.output target_lang=zh"
python ~/GOD.util/unk_tool/alignment_parser.py -s $1 -p $2 -t $3 -m second -o output
sed -i 's/\(<unk2>\s*\)\+/<unk2> /g' output
python ~/GOD.util/unk_tool/assert_unk2_nums.py < output > 2
mv 2 output
sed -n '0~2p' output > unk_t
sed -n '1~2p' output > unk_s
rm output
