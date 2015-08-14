from bdp.node import *

# mul_block = block("x", size=p(2,2), shape='circle')()
# path([mul_block.n(0.25), mul_block.n(0.25) - (1,1)])()
# mul_block = block(size=p(2,2))()
# path([mul_block.n(0.25), mul_block.n(0.25) + (0,5)])()



mul_block = block("x", size=p(2,2), shape='circle')
add_block = block("+", size=p(2,2), shape='circle')
 
mul = []

evaluator = block(dotted=True)

fifo_blk = block(size=p(4,4))
inst_fifo = []
inst_fifo.append(fifo_blk(t="$I_{i}$", size=p(6,4), p=evaluator.p + (13, 3))())
inst_fifo.append(fifo_blk(t="$I_{i+1}$").right(prev(1), 0)())
inst_fifo.append(fifo_blk(t="$I_{i+2}$").right(prev(1), 0)())
inst_fifo.append(fifo_blk(t="$\cdot\cdot\cdot$").right(prev(1), 0)())
inst_fifo.append(fifo_blk(t="$I_{i+N_P-1}$").right(prev(1), 0)())
text("Instance Queue", margin=p(0,0)).align(inst_fifo[0].n(), prev().s())()

bus = path(double=True, thick=False)
bus_text = text(font="small", margin=p(0.4,0.2))

bus([inst_fifo[0].w(0.5) - (16,0), inst_fifo[0].w(0.5)], style='->')()
bus_text(r"Instance \\ Input").align_y(prev(1)[1], prev().s()).align_x(evaluator.p)()

inp_coef_tmpl = block(size=p(3,2), border=False, text_align="ce", node_sep=(1, 0.5))
inp_coefs = []

inp_coefs.append(inp_coef_tmpl("$A_{1}$").below(inst_fifo[0], 1).align_x(inst_fifo[0].s(1.0) - (1,0), prev().s(1.0))())
inp_coefs.append(inp_coef_tmpl("$a_{1}$").below(prev(1))())
inp_coefs.append(inp_coef_tmpl("$A_{2}$").below(prev(1), 1)())
inp_coefs.append(inp_coef_tmpl("$a_{2}$").below(prev(1))())

inp_coefs.append(inp_coef_tmpl("$A_{N^{M}_{A}-1}$").below(prev(1), 2)())
inp_coefs.append(inp_coef_tmpl("$a_{N^{M}_{A}-1}$").below(prev(1))())
inp_coefs.append(inp_coef_tmpl("$A_{N^{M}_{A}}$").below(prev(1), 1)())
inp_coefs.append(inp_coef_tmpl("$a_{N^{M}_{A}}$").below(prev(1))())

for i in range(len(inp_coefs)//2):
    path([inst_fifo[0].s(1), inp_coefs[2*i].w(0.5)], def_routing='|-', style='->')()

 
for i in range(len(inp_coefs)//2):
    mul.append(mul_block.align_y(mid(inp_coefs[2*i].p, inp_coefs[2*i+1].p)).align_x(inst_fifo[1].c(), mul_block.c())())
    path([inp_coefs[2*i].c(), mul[i].c()], shorten=(2, 1.5), style='->', thick=True)()
    path([inp_coefs[2*i+1].c(), mul[i].c()], shorten=(2, 1.5), style='->', thick=True)()
    
text(r"$\cdot$ \\ $\cdot$ \\ $\cdot$", font="normalsize").align_x(mul[1].c(), prev().c()).align_y(mid(mul[1].c(), mul[2].c()), prev().c())()
  
add = []
  
for i in range(len(mul)//2):
    add.append(add_block.align_y(mid(mul[2*i].p, mul[2*i+1].p)).align_x(inst_fifo[2].c(), add_block.c())())
    block(size=p(0.3, 1.5)).align(mid(add[i].c(), mul[2*i].c()), prev().c())()
    path([mul[2*i].c(), add[i].c()], shorten=(1.2, 2.8), style='->', thick=True)()
    path([mul[2*i].c(), add[i].c()], shorten=(2.8, 1.2), style='->', thick=True)()

#     path([mul[2*i+1].c(), add[i].c()], shorten=(1.5, 1.5), style='->', thick=True)()
    block(size=p(0.3, 1.5)).align(mid(add[i].c(), mul[2*i+1].c()), prev().c())()
    path([mul[2*i+1].c(), add[i].c()], shorten=(1.2, 2.8), style='->', thick=True)()
    path([mul[2*i+1].c(), add[i].c()], shorten=(2.8, 1.2), style='->', thick=True)()
    

add.append(add_block.align_y(mid(add[0].p, add[1].p)).align_x(inst_fifo[4].c(), add_block.c())())
  
for i in range(2):
#     path([add[i].c(), add[2].c()], shorten=(1.5, 6.5), style='->', thick=True)()
    block(size=p(0.3, 1.5)).align(mid(add[i].c(), mul[2*i].c()), prev().c())()
    path([add[i].c(), add[2].c()], shorten=(1.2, 7.6), style='->', thick=True)()
    path([add[i].c(), add[2].c()], shorten=(7.6, 1.2), style='->', thick=True)()

    text(t="$\cdot\cdot\cdot$").align(mid(add[i].c(), add[2].c()), prev().c())()
#     path([add[i].c(), add[2].c()], shorten=(6.5, 1.5), style='->', thick=True)()
    
block(size=p(0.3, 1.5)).align(add[0].c() + (2.0, 1.2), prev().c())()
block(size=p(0.3, 1.5)).align(add[1].c() + (2.0, -1.2), prev().c())()

block(size=p(0.3, 1.5)).align(add[2].c() - (2.0, 1.2), prev().c())()
block(size=p(0.3, 1.5)).align(add[2].c() - (2.0, -1.2), prev().c())()

fifo_blk = block(size=p(4,8), conn_sep=2)

node_fifo = []
node_fifo.append(fifo_blk(t="$N_{i}$", size=p(6,8)).below(inp_coefs[7], 6).align_x(inst_fifo[0].p)())
node_fifo.append(fifo_blk(t="$N_{i+1}$").right(prev(1), 0)())
node_fifo.append(fifo_blk(t="$N_{i+2}$").right(prev(1), 0)())
node_fifo.append(fifo_blk(t="$\cdot\cdot\cdot$").right(prev(1), 0)())
node_fifo.append(fifo_blk(t="$N_{i+N_{P}-1}$").right(prev(1), 0)())
text("Node Queue", margin=p(0,0)).align(node_fifo[0].n(2), prev().s())()

for n, i in zip(node_fifo, inst_fifo):
    path([i.s(1.0), n.n(1.0)], dotted=True)()

mem_intf = block(r"DT Memory Interface", size=p(6,6)).align(node_fifo[0].n() - (2,1), prev().s(1.0))()
bus([mem_intf.w(4) - (8, 0), mem_intf.w(4)], style='<->')()
bus([mem_intf.s(4), node_fifo[0].w(1)], def_routing='|-', style='->')()
bus_text(r"Child \\ IDs").align(prev(1)[2], prev().s(1.0))()
bus([mem_intf.s(3), node_fifo[0].w(2)], def_routing='|-', style='->')()
bus_text(r"Leaf IDs").align(prev(1)[2], prev().s(1.0))()
path([mem_intf.e(5), node_fifo[0].n(1)], def_routing='-|', style='->')()
bus_text("$threshold$").align(prev(1)[0], prev().s())()

# bus_text("child data: left ID, right ID").align(mem_intf.e(4) + (1,0), prev().n())()

path([mem_intf.w(2) - (8, 0), mem_intf.w(2)], style='->')()
bus_text(r"Child ID \\ Input").align_y(prev(1)[0], prev().s()).align_x(evaluator.p)()

for i in range(len(inp_coefs)//2):
    path([mem_intf.e(3), mem_intf.e(3) + (1,0), inp_coefs[2*i+1].w(0.5)], def_routing='|-', style='->', dotted=True)()

path([node_fifo[0].w(3) - (16, 0), node_fifo[0].w(3)], style='->')()
bus_text(r"Leaf ID \\ Input").align_y(prev(1)[0], prev().s()).align_x(evaluator.p)()

comp = block("$\geq$", p(4,4), text_font="Large").right(add[-1], 4).align_y(add[-1].c(), prev().w(1))()
path([add[-1].e(0.5), comp.w(1)], style='->', shorten=(0.5, 0))()
path([node_fifo[-1].n(0.5), comp.w(3)], def_routing='|-', style='->')()
bus_text("$threshold$").align(comp.w(3), prev().n(1.0))()
bus_text("$\sum_{i=1}^{n}a_{i}\cdot A_{i}$").align(comp.w(1) + (0.5,-1), prev().s(1.0))()

mux_tmpl = block("MUX", p(4,4), text_font="Large")

mux = mux_tmpl.right(comp, 2)()

bus([node_fifo[-1].e(1), mux.s(1)], def_routing='-|', style='->')()
bus_text(r"Child IDs").align(prev(1)[0], prev().s())()
bus([node_fifo[-1].e(2), mux.s(3)], def_routing='-|', style='->')()
bus_text(r"Leaf IDs").align(prev(1)[0], prev().s())()

path([comp.e(0.5), mux.w(0.5)], style='->')()

mux2 = mux_tmpl.over(mux, 2).align_x(mux.e(), mux_tmpl.c())()
path([mux.n(3), mux2.s(1)], style='->')()
path([node_fifo[-1].e(3), mux2.s(3)], def_routing='-|', style='->')()
bus_text(r"Leaf ID Input").align(prev(1)[0], prev().s())()

comp_zero = block("$>0$", p(3,2), text_font="Large").right(mux, 2)()
path([node_fifo[-1].e(3), comp_zero.s(0.5)], def_routing='-|', style='->')()

path([comp_zero.n(0.5), mux2.e(0.5)], def_routing='|-', style='->')()

evaluator.size[0] = (comp_zero.e() + (1, 0) - evaluator.p)[0]
evaluator.size[1] = (node_fifo[-1].s(1.0) + (1,1) - evaluator.p)[1]
evaluator("NTE", text_font="Large", text_align="nw")()

path([mux2.n(0.5), p(evaluator.e()[0] + 2, mux2.n()[1] -2)], def_routing='|-', style='->')()
bus_text("Leaf ID Output").align_y(prev(1)[1], prev().s()).align_x(evaluator.e(), prev().s(1.0))()
path([mux.n(1), p(evaluator.e()[0] + 2, mux2.n()[1] -4)], def_routing='|-', style='->')()
bus_text("Child ID Output").align_y(prev(1)[1], prev().s()).align_x(evaluator.e(), prev().s(1.0))()

bus([inst_fifo[-1].e(0.5), p(evaluator.e()[0] + 2, inst_fifo[-1].c()[1])], style='->')()
bus_text("Instance Output").align_y(prev(1)[1], prev().s()).align_x(evaluator.e(), prev().s(1.0))()