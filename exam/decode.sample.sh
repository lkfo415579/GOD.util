cat $1 | ~/competence/build/marian-decoder -c $2/model_revo.npz.best-translation.npz.decoder.yml -b 10 --mini-batch 40 \
--output-sampling -d $3 -o output.txt --qkv-model false --maxi-batch 2 --max-length 150 --max-length-crop
