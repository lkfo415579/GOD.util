import codecs
import sys
if len(sys.argv) == 1:
    print "Usage : python main.py file error_line > output_file"
    sys.exit()

sys.stdout = codecs.getwriter("UTF-8")(sys.stdout)
f1 = codecs.open(sys.argv[1], "r", encoding='utf8').readlines()
error = codecs.open(sys.argv[2], "r", encoding='utf8').readlines()

error = [int(x.split(":")[0]) - 1 for x in error]

for i, line in enumerate(f1):
    if i not in error:
        sys.stdout.write(line)
