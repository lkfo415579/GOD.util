# -*- encoding=utf-8 -*-
s = "Yeah , he ' s just - -@@ he ' s - -@@ he ' s - -@@ he ' s - -@@ he ' s - -@@ he ' s - -@@"
# s = "Yeah , he ' s just - -@@ he ' s - -@@ he ' s"


def f(cur_str, s):
    step = len(cur_str)
    s = s[step:]
    # print "=" * 100 + "\n", cur_str, s
    count = 0
    for i in range(0, len(s), step):
        t = []
        t.extend(s[i:i + step])
        # for j in range(step):
        #     if i + j < len(s):
        #         t.append(s[i + j])
        # print "T:", t
        if cur_str == t:
            count += 1
        else:
            break
    # print "C:", count
    return count


def con(s):
    s = s.split()
    s = s[::-1]
    cur_str = []
    res = []
    for i, char in enumerate(s):
        cur_str.append(char)
        count = f(cur_str, s)
        if count:
            res.append((count, cur_str[:]))
    return res

print con(s)

