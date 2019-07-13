cat $1 | ~/marian-dev/build/marian-decoder -c $2/model_revo.npz.decoder.yml -b 6 --mini-batch 100 -d $3 -o output
