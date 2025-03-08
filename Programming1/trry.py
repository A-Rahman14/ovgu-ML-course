from numpy import append


hlist = []
blist = []
tlist = []
holz = []
h=200
while (h<260):
    b=200
    while (b<410):
        t=200
        while(t<410):
            if ((h*b*t) == 22500000):
                hlist.append(h)
                blist.append(b)
                tlist.append(t)
            t = t + 10
        b = b + 10
    h = h + 10

i=0
while(i<len(hlist)):
    sum=0
    sum+=hlist[i]*blist[i]*2*3
    sum+=blist[i]*tlist[i]*2*3
    sum+=tlist[i]*hlist[i]*2*3
    holz.append(sum/1000000)
    i += 1

i=0
while(i<len(hlist)):
    print("Hohe :", hlist[i], "cm")
    print("Breite :", blist[i], "cm")
    print("Tiefe :", tlist[i], "cm")
    print("Holz :", holz[i], "m^3\n")
    i += 1