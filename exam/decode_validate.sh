cat $1 | ~/marians/competence-gpu/cmake-build-debug/marian-decoder -c $3/model_revo.npz.best-translation.npz.decoder.yml \
-b 6 --mini-batch 100 -d 0 -o output.txt
cat output.txt | sed 's/@@ //g' \
    | ~/GOD.util/moses-scripts/scripts/generic/multi-bleu.perl -lc $2 \
    | sed -r 's/BLEU = ([0-9.]+),.*/\1/'
