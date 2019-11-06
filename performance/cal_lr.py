print "please input warm up step"
warm_up = float(raw_input())
print "please input model dim"
model_dim = float(raw_input())
print "(model_dim ** -0.5) * ((warm_up * warm_up) ** -1.5)"
base_lr = (model_dim ** -0.5) * warm_up * warm_up ** -1.5
for i in range(1, 10):
    i = float(i)
    print "%fx lr: %f" % (i, i * base_lr)
