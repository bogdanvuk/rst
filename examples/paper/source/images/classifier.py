from bdp.node import *

def make_nte(name, pos):
    nte = block(size=p(15,9), p=pos)
    pin_text = text(font='footnotesize', margin=(0.1, 0))
    pin_text("Instance Input").align(nte.w(2), prev().w(0.5))()
    pin_text("Leaf ID Input").align(nte.w(4), prev().w(0.5))()
    pin_text("Child ID Input").align(nte.w(5), prev().w(0.5))()
    
    pin_text("Instance Output").align(nte.e(2), prev().e(0.5))()
    pin_text("Leaf ID Output").align(nte.e(4), prev().e(0.5))()
    pin_text("Child ID Output").align(nte.e(5), prev().e(0.5))()
    
    pin_text("DT Memory Interface").align(nte.w(7), prev().w(0.5))()
    
    nte()
    text("NTE " + name).align(nte.n(0), prev().s(0))()
    
    return nte

nte = []
nte.append(make_nte('$L_{1}$', p(0, 0)))
nte.append(make_nte('$L_{2}$', p(18, 0)))
nte.append(make_nte('$L_{D^{M}}$', p(44, 0)))

bus = path(double=True, thick=False)
bus_text = text(font="tiny", margin=p(0,0))

bus([nte[0].e(2), nte[1].w(2)], style='->')()
path([nte[0].e(4), nte[1].w(4)], style='->')()
path([nte[0].e(5), nte[1].w(5)], style='->')()

bus([nte[1].e(2), nte[1].e(2) + (3,0)], style='->')()
path([nte[1].e(4), nte[1].e(4) + (3,0)], style='->')()
path([nte[1].e(5), nte[1].e(5) + (3,0)], style='->')()

bus([nte[2].w(2) - (3,0), nte[2].w(2)], style='->')()
path([nte[2].w(4) - (3,0), nte[2].w(4)], style='->')()
path([nte[2].w(5) - (3,0), nte[2].w(5)], style='->')()

text("$\cdot\cdot\cdot$", font="huge").align(mid(nte[1].c(), nte[2].c()), prev().c())()

bus([nte[0].w(2) - (6, 0), nte[0].w(2)], style='->')()
path([nte[0].w(4) - (2, 0), nte[0].w(4)], style='->')()
text("0").align(prev(1)[0], prev().e(0.5))()
path([nte[0].w(5) - (2, 0), nte[0].w(5)], style='->')()
text("0").align(prev(1)[0], prev().e(0.5))()

for i in range(3):
    bus([nte[i].w(7) + (-2, 5), nte[i].w(7)], def_routing='|-', style='->')()

bus([nte[2].e(2), nte[2].e(2) + (4, 0)], style='->')()
path([nte[2].e(4), nte[2].e(4) + (4, 0)], style='->')()
path([nte[2].e(5), nte[2].e(5) + (1, 0)])()
text("x", margin=(0,0)).align(prev(1)[1] - (0.5, 0), prev().w(0.5))()

block("Classifier", nte[2].s(1.0) - nte[0].n() + (6,6), text_align="nw", font='Large', dotted=True, margin=(1, 0.4)).align(nte[0].n() - (4, 4), prev().n())()


# block.size = p(8, 4)
# block.node_sep = (4,2)
#  
# qu_l0 = block("Instance queue $L_{0}$")()
# eval_l0 = block("Node test evaluation $L_{0}$").below(qu_l0)()
#  
# qu_l1 = block("Instance queue $L_{1}$").right(qu_l0)()
# eval_l1 = block("Node test evaluation $L_{1}$").right(eval_l0)()
#  
# qu_lD = block("Instance queue $L_{D}$").right(qu_l1, 2)()
# eval_lD = block("Node test evaluation $L_{D}$").right(eval_l1, 2)()
#  
# text("$\cdot\cdot\cdot$", font="huge").align(mid(qu_l1.c(), qu_lD.c()), prev().c())()
# text("$\cdot\cdot\cdot$", font="huge").align(mid(eval_l1.c(), eval_lD.c()), prev().c())()
# 
# bus = path(double=True)
# wire = path(ultra_thick=True)
# bus_text = text(font="scriptsize")
# 
# wire([qu_l0.w(1) - (3,0), qu_l0.w(1)])()
# bus_text("Instance attributes \\\\ vector $\mathbf{A}$", text_align='right').align(prev(1)[0], prev().e(0.5))()
# wire([qu_l0.w(3) - (3,0), qu_l0.w(3)])()
# bus_text("Instance class \\\\ $C$", text_align='right').align(prev(1)[0], prev().e(0.5))()