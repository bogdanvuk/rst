from bdp import *

comp = block(size=p(6,4), nodesep=(2,2))
bus_cap = cap(length=0.8, width=1.3, inset=0, type='Stealth')
bus = path(style=(bus_cap, bus_cap), line_width=0.7, double=True, border_width=0.1, shorten = [0.2, 0.2])
bus_text = text(font="\\scriptsize", margin=p(0,0.5))

pl = block("EFTIP hardware co-processor", text_margin=p(0.5, 0.5), alignment="nw", dotted=True, group='tight', group_margin=[p(1,2), p(1,2)])
pl += comp("Control Unit")
fig << text("irq").left(pl['Co'], 3)
pl += comp("Training Set Memory").right(pl['Co'], 1.5)
pl += bus(pl['Co'].e(0.5), pl['Tr'].w(0.5))

pl += comp("Accuracy Calculator").right(pl['Tr'])
pl += bus(pl['Ac'].n(0.5), pl['Ac'].n(0.5) - (0,1), pl['Co'].n(0.5), style=('', bus_cap), routedef='-|')
 
t_nte = block(size=(4, 2), nodesep=(3,1), font='\\footnotesize')


dt_mem = block("DT Memory Array", text_margin=p(0, 1), alignment="bc", dotted=True, group='tight', text_font='\\footnotesize', group_margin=[p(1,1), p(1,1)])
 
dt_mem += t_nte("$L_1$").below(pl['Co']).alignx(pl['Co'].s(3))
dt_mem += t_nte("$L_2$").below(dt_mem['$L_1'])
dt_mem += t_nte("$L_{D^M}$").below(dt_mem['$L_2'], 3)

pl += text(r"$\cdot\cdot\cdot$", font='\\footnotesize').align(mid(dt_mem['$L_2'].c(), dt_mem['$L_{D^M}'].c()), prev().c())

pl['dt_mem'] = dt_mem

dt_mem_net = net()

for d in dt_mem:
    dt_mem_net += bus(pl['Co'].s(1), dt_mem[d].w(0.5), routedef='|-')
    
pl += dt_mem_net
 
nte = block("Classifier", text_margin=p(0, 1), alignment="bc", dotted=True, group='tight', text_font='\\footnotesize', group_margin=[p(1,1), p(1,1)])

nte += t_nte("$NTE_1$").right(dt_mem[0])
nte += t_nte("$NTE_2$").right(dt_mem[1])
pl += bus(nte[0].s(0.5), nte[1].n(0.5), style=('', bus_cap))
nte += t_nte("$NTE_{D^M}$").right(dt_mem[2])
pl += bus(nte[1].s(0.5), nte[1].s(0.5) + (0,1), style=('', bus_cap))
pl += bus(nte[2].n(0.5), nte[2].n(0.5) - (0,1), style=(bus_cap, ''))
pl += text('$\cdot\cdot\cdot$').align(mid(nte[1].c(), nte[2].c()), prev().c())

pl += nte

pl += bus(nte[2].e(0.5), pl['Ac'].s(0.5), style=('', bus_cap), routedef='-|')
 
for n, d in zip(nte, dt_mem):
    pl += bus(dt_mem[d].e(0.5), nte[n].w(0.5), style=('', bus_cap))
    
     
pl += bus(pl['Tr'].s(0.5), nte[0].n(0.5), style=('', bus_cap))

fig << pl
#render_fig(fig, './eftip.pdf')

