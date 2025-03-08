import argparse
import csv
import math

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=argparse.FileType('r'))
parser.add_argument('--k', type=float)
args = parser.parse_args()


def calculateweight(a, b, c):
    weight = (a - b) / (a - c)
    return weight


def classification(c, kN):
    cases = [0, 0]
    dk = (math.sqrt((c[1] - kN[0][1]) * 2 + (c[2] - kN[0][2]) * 2))
    dOne = (math.sqrt((c[1] - kN[len(kN) - 1][1]) * 2 + (c[2] - kN[len(kN) - 1][2]) * 2))
    if dk == dOne:
        for n in kN:
            if n[0] == 'A':
                cases[0] += 1
            else:
                cases[1] += 1
    else:
        for n in kN:
            di = (math.sqrt((c[1] - n[1]) * 2 + (c[2] - n[2]) * 2))
            weight_ = calculateweight(dk, di, dOne)
            if n[0] == 'A':
                cases[0] += weight_
            else:
                cases[1] += weight_

    if cases[0] > cases[1]:
        return 'A'
    else:
        return 'B'


def insertK(arr, item, c, k):
    distance = (math.sqrt((c[1] - item[1]) * 2 + (c[2] - item[2]) * 2))
    inserted = False

    for i in range(len(arr)):
        if distance >= (math.sqrt((c[1] - arr[i][1]) * 2 + (c[2] - arr[i][2]) * 2)):
            arr.insert(i, item)
            inserted = True
            break
    if len(arr) > k:
        arr.remove(arr[0])
    if not inserted:
        arr.append(item)

    return arr


def ibTwo(data):
    cb = [data[0]]
    data.pop(0)
    # classify every datapoint
    i = 0
    while i < len(data):
        c = data[i]
        # choose first case in cb as default nearest
        nC = cb[0]
        # check for nearest case in cb
        for cbC in cb:
            if (math.sqrt((c[1] - cbC[1]) * 2 + (c[2] - cbC[2]) * 2)) < (
                    math.sqrt((c[1] - nC[1]) * 2 + (c[2] - nC[2]) * 2)):
                nC = cbC
        # check if misclassified, if correct nothing happens
        if c[0] != nC[0]:
            cb.append(c)
            data.pop(i)
        i += 1
    return data, cb


data = []
# form csv to an array
reader = csv.reader(args.data)
for row in reader:
    data.append(row)
# turn the strings to floats
for row in range(len(data)):
    for item in range(1, len(data[row])):
        data[row][item] = float(data[row][item])

data, cb = ibTwo(data)
total = 0
for point in data:
    kN = []
    for c in cb:
        if len(kN) < args.k:
            kN = insertK(kN, c, point, args.k)
        elif (math.sqrt((point[1] - c[1]) * 2 + (point[2] - c[2]) * 2)) <\
                (math.sqrt((point[1] - kN[0][1]) * 2 + (point[2] - kN[0][2]) * 2)):
            kN = insertK(kN, c, point, args.k)
    clas = classification(point, kN)
    if clas != point[0]:
        total += 1

print(total)
for x in cb:
    s = ""
    for step, entry in enumerate(x):
        s += str(entry)
        if step != len(x) - 1:
            s += ","
    print(s)
