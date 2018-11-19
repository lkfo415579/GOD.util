import codecs
import sys
if len(sys.argv) == 1:
    print "Usage : python main.py file error_line split_sym[:] output_option[default:file|err](1 or 0) > output_file"
    sys.exit()

sys.stdout = codecs.getwriter("UTF-8")(sys.stdout)
f1 = codecs.open(sys.argv[1], "r", encoding='utf8').readlines()
error = codecs.open(sys.argv[2], "r", encoding='utf8').readlines()

if len(sys.argv) < 4:
    symbol = ':'
    # determin start from 1
    error = [int(x.split(symbol)[0]) - 1 for x in error]
else:
    symbol = sys.argv[3]
    # start from 0
    error = [int(x.split(symbol)[0]) for x in error]

if len(sys.argv) < 5:
    output_file = True
else:
    output_file = False


if output_file:
    for i, line in enumerate(f1):
        if i not in error:
            sys.stdout.write(line)
        else:
            error.remove(i)

else:
    for i in error:
        line = f1[i]
        sys.stdout.write(line)
