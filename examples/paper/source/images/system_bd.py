from bdp.node import *

ps = block("Processing System", size=p(16,20), margin=p(0.5, 0.5), text_align="nw", dotted=True)()

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

pl = block("EFTIP hardware co-processor", size=p(24,34), margin=p(0.5, 0.5), text_align="nw", dotted=True).right(ps, 2)()

cu = comp("Control Unit").align_x(pl.r(1, 0)).align_y(cpu.p)()
bus([intercon.e(2), cu.w(2)], style='<->')()
t_axi = bus_text("AXI4").align(prev(1).pos(0.5), prev().s(0.5))()


inst_mem = comp("Training Set Memory").right(cu)()
bus([cu.e(0.5), inst_mem.w(0.5)], style='<->')()

fit_calc = comp("Accuracy Calculator").right(inst_mem)()
bus([fit_calc.n(0.5), fit_calc.n(0.5) - (0,1), cu.n(0.5)], style='->', def_routing='-|')()

t_nte = block(size=(5, 6), node_sep=(4,1)) #, text_font='footnotesize')

t_dt_mem = t_nte(text_align="cw", margin=p(0.5, 0))
t_dt_submem = block(size=t_nte.size/2, dotted=True)

dt_mem = []
dt_mem.append(t_dt_mem("$L_1$").below(cu).align_x(cu.s(3))())
dt_mem.append(t_dt_mem("$L_2$").below(dt_mem[0])())
dt_mem.append(t_dt_mem("$L_{D^M}$").below(dt_mem[1], 3)())

for d in dt_mem:
    t_dt_submem("coef").align(d.e(0), prev().e(0))()
    t_dt_submem("topo").align(d.e(1.0), prev().e(1.0))()

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

mem_bus_text = bus_text(margin=p(0,0.2))

for n, d in zip(nte, dt_mem):
    for i in range(2):
        for (j, name, style) in zip(range(2), ['addr', 'data'], ['<-', '->']):
            pos = i*3 + j + 1
            bus([d.e(pos), n.w(pos)], style=style)()
            mem_bus_text(name).align(prev(1).pos(0.5), prev().s(0.5))()

        # bus([d.e(2), n.w(i*3 + 2)], style='->')()
        # mem_bus_text("data").align(prev(1).pos(0.5), prev().s(0.5))()
#    bus([d.e(4), n.w(4)], style='<-')()
#    bus([d.e(5), n.w(5)], style='->')()

bus([inst_mem.e(0.5), (nte[0].n(0.5)[0], inst_mem.e(0.5)[1]), nte[0].n(0.5)], style='->', def_routing='-|')()
