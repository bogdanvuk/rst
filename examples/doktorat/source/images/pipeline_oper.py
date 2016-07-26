from bdp import *
from eftirun_findt import dt
from dt_classify import classify
from dtdtools import dt_for_hw
import copy

pipstage = block(size=p(7,3), nodesep=p(0,0))

import random
import attrspace_plot

def coef2hex(val):
    return '{:04X}'.format(int(val) & (2**16-1))

random.seed(28)
fn = "/home/bvukobratovic/projects/rst/examples/doktorat/source/data/vene.csv"
attr, cls = attrspace_plot.load_arff(fn)

tset = [[float(a) for a in attr[i]] for i in random.sample(range(len(attr)), 9)]

insttext = [r"$[\mathtt{{{}}}, \mathtt{{{}}}]$".format(*[coef2hex(xi*32768) for xi in x])
           for x in tset[0:9]]

dt = copy.deepcopy(dt)
dt_for_hw(dt, 0)

nodetext = []
for i in range(3):
    for j in range(3):
        n = classify(tset[i*3+j], dt, max_level=i)
        nodetext.append(str(n['id']))

print(nodetext)

# piptext = [
#     [
#         ("-", '0'),
#         ("-", '0'),
#         ("-", '0'),
#     ],
#     [
#         ("-", '0'),
#         ("-", '0'),
#         ("-", '0'),
#     ],
#     [
#         ("-", '0'),
#         ("-", '0'),
#         ("-", '0'),
#     ],
# ]

# inst_fifo = fifo_blk("Instance Queue")
# for i,t in enumerate(inst_fifo_text):
#     if i == 0:
#         inst_fifo += fifo_item(t, size=p(10,2))
#     else:
#         inst_fifo += fifo_item(t).right(inst_fifo[-1])

# nte += inst_fifo
