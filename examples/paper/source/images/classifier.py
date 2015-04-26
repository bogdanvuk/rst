from bdp.node import *

block.size = p(8, 4)
block.node_sep = (4,2)
 
qu_l0 = block("Instance queue $L_{0}$")()
eval_l0 = block("Node test evaluation $L_{0}$").bellow(qu_l0)()
 
qu_l1 = block("Instance queue $L_{1}$").right(qu_l0)()
eval_l1 = block("Node test evaluation $L_{1}$").right(eval_l0)()
 
qu_lD = block("Instance queue $L_{D}$").right(qu_l1, 2)()
eval_lD = block("Node test evaluation $L_{D}$").right(eval_l1, 2)()
 
text("$\cdot\cdot\cdot$", font="huge").align(mid(qu_l1.c(), qu_lD.c()), prev().c())()
text("$\cdot\cdot\cdot$", font="huge").align(mid(eval_l1.c(), eval_lD.c()), prev().c())()

bus = path(double=True)
wire = path(ultra_thick=True)
bus_text = text(font="scriptsize")

wire([qu_l0.w(1) - (3,0), qu_l0.w(1)])()
bus_text("Instance attributes \\\\ vector $\mathbf{A}$").align(prev(1)[0], prev().e(0.5))()
wire([qu_l0.w(3) - (3,0), qu_l0.w(3)])()
bus_text("Instance class \\\\ $C$").align(prev(1)[0], prev().e(0.5))()