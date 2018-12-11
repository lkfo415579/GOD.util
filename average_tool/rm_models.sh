# rm model_revo_amun.iter{50000..$1..50000}.npz
rm `seq -f 'model_revo_amun.iter%.0f.npz' 50000 50000 ${1}00000`
