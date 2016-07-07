import classify
import cmath
import random
import dt2plot

dt = {
    "0": {"lvl": 0, "id": 0,"cls": 0,"left": "1","right": "2","thr": 1,"coeffs": [2,0]},
    "1": {"lvl": 1, "id": 1,"cls": 0,"left": "3","right": "4","thr": -3,"coeffs": [8,-10]},
    "2": {"lvl": 1, "id": 2,"cls": 0,"left": "5","right": "6","thr": 1,"coeffs": [8,-10]},
    "3": {"lvl": 2, "id": 3,"cls": 1,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "4": {"lvl": 2, "id": 4,"cls": 0,"left": "7","right": "8","thr": 7,"coeffs": [8,10]},
    "5": {"lvl": 2, "id": 5,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "6": {"lvl": 2, "id": 6,"cls": 0,"left": "9","right": "10","thr": 11,"coeffs": [8,10]},
    "7": {"lvl": 3, "id": 7,"cls": 1,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "8": {"lvl": 3, "id": 8,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "9": {"lvl": 3, "id": 9,"cls": 1,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []},
    "10": {"lvl": 3, "id": 10,"cls": 2,"left": "-1","right": "-1","thr": 0.00000,"coeffs": []}
}

fn = "../data/yingyang.csv"
train_set_size = 200
r_max = 0.46
train_set = []
for i in range(train_set_size):
    crnd = cmath.rect(random.uniform(0.05, r_max), random.uniform(0, 2*cmath.pi))
    train_set.append([crnd.real + 0.5, crnd.imag + 0.5, 0])

classes = classify.classify(dt, train_set)
for i, c in zip(train_set, classes):
    i[-1] = c

import csv
with open(fn, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in train_set:
        spamwriter.writerow(i)

dt2plot.plot(dt, "oblique_dt_traversal_attrspace.pdf", "../data/yingyang.csv")
