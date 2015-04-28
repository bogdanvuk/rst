from bdp.node import *

ps = block(size=p(10,16), t="Processing System", margin=p(0.5, 0.5), text_align="nw")()

comp = block(size=p(6,4), node_sep=(3,3))
bus = path(double=True, thick=False)
bus_text = text(font="tiny", margin=p(0,0))

# ps_comp = comp(ps.r(0, 3), "CPU").align_x(comp.c(), ps.c())  
  
cpu = comp("CPU").align_x(ps.c(), prev().c()).align_y(ps.w(3))()
mem = comp("Memory").below(cpu)()
mem_bus = bus([cpu.s(0.5), mem.n(0.5)], style='<->')()


pl = block(size=p(32,16), t="Programmable Logic", margin=p(0.5, 0.5), text_align="nw").right(ps, 2)()

cu = comp("Control Unit").align_x(pl.r(2, 0)).align_y(cpu.p)()
inst_mem = comp("Training Set Memory").below(cu)()

dt_mem_array = comp("DT Memory Array").right(cu)()

for i in range(dt_mem_array.size[0]):
    path([dt_mem_array.n(i+1), dt_mem_array.s(i+1)], dotted=True)()
    
dt_class = comp("Classifier").below(dt_mem_array)()
for i in range(dt_class.size[0]):
    path([dt_class.n(i+1), dt_class.s(i+1)], dotted=True)()
    
for i in [0, 1]:
    bus_text("$L_{" + str(i) + '}$').align(dt_class.s(i), prev().n())()
bus_text('$L_{D-1}$').align(dt_class.s(5), prev().n())()
text('$\cdot\cdot\cdot$').align(mid(prev(2).e(0.5), prev(1).w(0.5)), prev().c())()

for i in [0, 1]:
    bus([dt_mem_array.s(i) + (0.5, 0), dt_class.n(i) + (0.5, 0)], style='<->')()
bus([dt_mem_array.s(5) + (0.5, 0), dt_class.n(5) + (0.5, 0)], style='<->')()
text('$\cdot\cdot\cdot$').align(mid(prev(2)[0], prev(1)[1]), prev().c())()
bus_text('PortB').align_x(prev(1).c(), prev().c()).align_y(dt_mem_array.s(), prev().n())()

bus([cu.e(0.5), dt_mem_array.w(0.5)], style='<->')()
bus_text("PortA").align(dt_mem_array.w(0.5), prev().s(1.0))()
 
bus([cpu.e(0.5), cu.w(0.5)], style='<->')()
t_axi = bus_text("AXI4").align(prev(1).pos(0.5), prev().s(0.5))()

bus([cu.s(0.5), inst_mem.n(0.5)], style='<->')()
bus_text("PortA").align(inst_mem.e(0.5), prev().n(0))()
bus([inst_mem.e(0.5), dt_class.w(0.5)], style='->')()
bus_text("PortB").align(inst_mem.n(0.5), prev().s(0))()

fit_calc = comp("Fitness Calculator").right(dt_class)()
bus([dt_class.e(0.5), fit_calc.w(0.5)], style='->')()
bus([fit_calc.n(0.5), cu.n(0.5) - (0,1), cu.n(0.5)], def_routing='|-', style='<->')()
