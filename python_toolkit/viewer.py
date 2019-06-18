import sys

f = open(sys.argv[1], 'rb')
buffer = f.read()
# buferr = list(buffer)
print "First \\x93NUMPY:", buffer.index('\x93')

a = ["{:02x}".format(ord(c)) for c in buffer]
print "52 index", a[52:70]
print "52 index buffer", list(buffer[52:70])

print len(buffer)
