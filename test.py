from data import *
y= 0
for k in I_automation:
    for l in J:
        for x in W:
            for i in I_automation:
                for j in J:
                    for w in W:
                        if (k, l, x) < (i, j, w) and not (l == j and x == w) and not (k == i and l == j): # avoids comparing the same process steps twice and avoids comparing two steps of the same wafer (j,w) because (2) already holds and avoids comparing the same process module in its same process step because (3) holds.
                               print(i,j,w,k,l,x)
                               y= y+ 1
print('y ist = ',y)