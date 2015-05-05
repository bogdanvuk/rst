from bdp.node import *

ps = block("Processing System", size=p(16,22), margin=p(0.5, 0.5), text_align="nw", dotted=True)()

comp = block(size=p(6,4), node_sep=(2,2))
ps_comp = block(size=p(6,6), node_sep=(2,3))
bus = path(double=True, thick=False)
bus_text = text(font="scriptsize", margin=p(0,0.5))

# ps_comp = comp(ps.r(0, 3), "CPU").align_x(comp.c(), ps.c())  
  
cpu = ps_comp("CPU").align(ps.r(1,3))()
mem_con = ps_comp("DDR3 Memory Controller").below(cpu)()

ddr3 = ps_comp("DDR3 Memory").left(mem_con)()
bus([ddr3.e(0.5), mem_con.w(0.5)], style='<->')()

intercon = block(r"AXI4 \\ Interconnect", mem_con.s(1.0)-cpu.n()).right(cpu)()
bus([cpu.e(2), intercon.w(2)], style='<->')()
t_axi = bus_text("AXI4").align(prev(1).pos(0.5), prev().s(0.5))()

bus([mem_con.e(0.5), palign(intercon.w(), mem_con.e(0.5))], style='<->')()
t_axi = bus_text("AXI4").align(prev(1).pos(0.5), prev().s(0.5))()

pl = block("EFTIP hardware co-processor", size=p(25,22), margin=p(0.5, 0.5), text_align="nw", dotted=True).right(ps, 2)()

cu = comp("Control Unit").align_x(pl.r(1, 0)).align_y(cpu.p)()
bus([intercon.e(2), cu.w(2)], style='<->')()
t_axi = bus_text("AXI4").align(prev(1).pos(0.5), prev().s(0.5))()


inst_mem = comp("Training Set Memory").right(cu, 1.5)()
bus([cu.e(0.5), inst_mem.w(0.5)], style='<->')()

fit_calc = comp("Fitness Calculator").right(inst_mem)()
bus([fit_calc.n(0.5), fit_calc.n(0.5) - (0,1), cu.n(0.5)], style='->', def_routing='-|')()

t_nte = block(size=(4, 2), node_sep=(3,1), text_font='footnotesize')

# nte = []
# nte.append(t_nte("$NTE_1$").right(inst_mem)())
# nte.append(t_nte("$NTE_2$").right(nte[0])())
# bus([nte[0].e(0.5), nte[1].w(0.5)], style='->')()
# 
# nte.append(t_nte("$NTE_{D^M}$").right(nte[1], 3)())
# bus([nte[1].e(0.5), nte[1].e(0.5) + (2,0)], style='->')()
# bus([nte[2].w(0.5), nte[2].w(0.5) - (2,0)], style='<-')()
# text('$\cdot\cdot\cdot$').align(mid(nte[1].c(), nte[2].c()), prev().c())()

dt_mem = []
dt_mem.append(t_nte("$L_1$").below(cu).align_x(cu.s(3))())
dt_mem.append(t_nte("$L_2$").below(dt_mem[0])())
dt_mem.append(t_nte("$L_{D^M}$").below(dt_mem[1], 3)())
text(r"$\cdot\cdot\cdot$", text_font='footnotesize').align(mid(dt_mem[1].c(), dt_mem[2].c()), prev().c())()

block("DT Memory Array", dt_mem[2].s(1.0) - dt_mem[0].n() + (2,2), dotted=True, text_font='footnotesize', text_align='bc').align(dt_mem[0].n() - (1,1))()

for d in dt_mem:
    bus([cu.s(1), d.w(0.5)], style='<->', def_routing='|-')()

nte = []
nte.append(t_nte("$NTE_1$").right(dt_mem[0])())
nte.append(t_nte("$NTE_2$").right(dt_mem[1])())
bus([nte[0].s(0.5), nte[1].n(0.5)], style='->')()
nte.append(t_nte("$NTE_{D^M}$").right(dt_mem[2])())
bus([nte[1].s(0.5), nte[1].s(0.5) + (0,1)], style='->')()
bus([nte[2].n(0.5), nte[2].n(0.5) - (0,1)], style='<-')()
text('$\cdot\cdot\cdot$').align(mid(nte[1].c(), nte[2].c()), prev().c())()

block("Classifier", nte[2].s(1.0) - nte[0].n() + (2,2), dotted=True, text_font='footnotesize', text_align='bc').align(nte[0].n() - (1,1))()

bus([nte[2].e(0.5), fit_calc.s(0.5)], style='->', def_routing='-|')()

for n, d in zip(nte, dt_mem):
    bus([d.e(0.5), n.w(0.5)], style='->')()
    
bus([inst_mem.s(0.5), nte[0].n(0.5)], style='->')()


















# 
#     
# dt_class = comp("Classifier").below(dt_mem_array)()
# for i in range(dt_class.size[0]):
#     path([dt_class.n(i+1), dt_class.s(i+1)], dotted=True)()

#     
# for i in [0, 1]:
#     bus_text("$L_{" + str(i+1) + '}$').align(dt_class.s(i), prev().n())()
# bus_text('$L_{D^{M}}$').align(dt_class.s(5), prev().n())()
# text('$\cdot\cdot\cdot$').align(mid(prev(2).e(0.5), prev(1).w(0.5)), prev().c())()
# 
# for i in [0, 1]:
#     bus([dt_mem_array.s(i) + (0.5, 0), dt_class.n(i) + (0.5, 0)], style='<->')()
# bus([dt_mem_array.s(5) + (0.5, 0), dt_class.n(5) + (0.5, 0)], style='<->')()
# text('$\cdot\cdot\cdot$').align(mid(prev(2)[1], prev(1)[0]), prev().c())()
# # bus_text('PortB').align_x(prev(1).c(), prev().c()).align_y(dt_mem_array.s(), prev().n())()
# 
# bus([cu.e(0.5), dt_mem_array.w(0.5)], style='<->')()
# # bus_text("PortA").align(dt_mem_array.w(0.5), prev().s(1.0))()
#  
# 
# bus([cu.s(0.5), inst_mem.n(0.5)], style='<->')()
# # bus_text("PortA").align(inst_mem.e(0.5), prev().n(0))()
# bus([inst_mem.e(0.5), dt_class.w(0.5)], style='->')()
# # bus_text("PortB").align(inst_mem.n(0.5), prev().s(0))()
# 
# fit_calc = comp("Fitness Calculator").right(dt_class)()
# bus([dt_class.e(0.5), fit_calc.w(0.5)], style='->')()
# bus([fit_calc.n(0.5), cu.n(0.5) - (0,1), cu.n(0.5)], def_routing='|-', style='<->')()
