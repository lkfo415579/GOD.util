print("please input warm up step")
warm_up = float(input())
# print "please input model dim"
# model_dim = float(raw_input())

def cal(model_dim):
    print ("WARM:%f, DIM:%f" % (warm_up, model_dim))
    print ("(model_dim ** -0.5) * ((warm_up * warm_up) ** -1.5)")
    base_lr = (model_dim ** -0.5) * warm_up * warm_up ** -1.5
    for i in range(1, 10):
        i = float(i)
        print ("%fx lr: %f" % (i, i * base_lr))
cal(512)
cal(1024)
