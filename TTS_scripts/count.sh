sox --i *.wav | grep -P '(\d+) samples' -o | cut -f1 -d ' ' > samples
awk '{sum+=} END {print sum}' samples-001
