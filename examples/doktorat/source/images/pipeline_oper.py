from bdp import *
from dt_classify import classify
from dtdtools import dt_for_hw
from eftirun_findt import dt
import copy
import random
import attrspace_plot

pipstage = block(size=p(5.5,3), nodesep=p(0,0), text_margin=p(0,0))
dt = copy.deepcopy(dt)
dt_for_hw(dt, 0)
fn = "/home/bvukobratovic/projects/rst/examples/doktorat/source/data/vene.csv"
attr, cls = attrspace_plot.load_arff(fn)

def coef2hex(val):
    return '{:04X}'.format(int(val) & (2**16-1))

def create_queue(qtext):
    queue = group(group="tight")
    for i in range(3):
        nte = group(group="tight")
        for j in range(3):
            stage_id = i*3 + j
            nte += pipstage(qtext[stage_id])

        for j in range(1,3):
            nte[j].align(nte[j-1].e(), nte[j].w())

        queue += nte

    for i in range(1,3):
        queue[i].align(queue[i-1].e() + p(1,0), queue[i].w())
        queue += path(queue[i].w(0.5), queue[i-1].e(0.5))

    queue += path(queue[2].e(0.5), poffx(2))
    if qtext[-1]:
        queue += text(qtext[-1]).align(queue[-1].pos(0.1), cur().s(0))

    queue += path(queue[0].w(0.5), poffx(-2))

    return queue

def plot_pipeline(w):
    random.seed(28)

    tset = [[float(a) for a in attr[i]] for i in reversed(random.sample(range(len(attr)), w.stop))]

    insttext = [r"$[\mathtt{{{}}}, \mathtt{{{}}}]$".format(*[coef2hex(xi*32768) for xi in x])
                for x in tset[w]]
    insttext += ['-'] * (10 - w.stop + w.start)

    instname = ["$I_{{{}}}$".format(i) for i in reversed(range(w.start, w.stop))]
    instname += [''] * (10 - w.stop + w.start)

    nodetext = []
    for i in range(3):
        for j in range(3):
            set_id = i*3+j + w.start
            if set_id < w.stop:
                n = classify(tset[set_id], dt, max_level=i)
                nodetext.append(str(n['id']))
            else:
                nodetext.append('-')

    if w.stop - w.start > 9:
        n = classify(tset[set_id], dt)
        nodetext.append(str(n['id']))
    else:
        nodetext.append('-')

    qinst = create_queue(insttext)
    if instname[-1]:
        qinst += text(instname[-1]).align(qinst[-2].n(0.5), cur().s(0.5))

    qnode = create_queue(nodetext)

    #pipeline = qnode
    pipeline = group(group="tight")
    pipeline += qinst
    pipeline += qnode.align(qinst[0].s() + p(0,2), qnode.n())

    for i in range(3):
        pipeline += text(r"$NTE_{}$".format(i)).align(mid(qinst[i].s(0.5), qnode[i].n(0.5)), cur().c())
        for j in range(3):
            stage_id = i*3 + j
            if instname[stage_id]:
                pipeline += text(instname[stage_id]).align(qinst[i][j].n(0.5), cur().s(0.5))

    pipeline += text("Instance Queue").over(qinst[0], 2).alignx(qinst.c(), cur().c())
    pipeline += text("Node Queue").below(qnode[0]).alignx(qinst.c(), cur().c())
    return pipeline

    # print(insttext)
    # print(nodetext)

#fig << plot_pipeline(slice(0,10))
#render_fig(fig)
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
