from bdp.node import *

block.text_font = 'large'
field = block(size=p(6,3))
bus = path(double=True, thick=False)
text.font = 'Large'

def make_row(pos, row_text, tmpl):
    tmpl.p = pos
    tmpl.left(tmpl, 0)
    objs = []
    for t in row_text:
        tmpl.right(tmpl, 0)
        dotted = t.startswith("$\cdot") or (t == '')
        if t.startswith("$\cdot"):
            objs.append(tmpl(t, dotted=dotted, text_font='tiny')())
        else:
            objs.append(tmpl(t, dotted=dotted)())

    return objs

coef_row_text = []
topo_row_text = []
for col_des in ['1', '2', 'N^{M}_{n}(l)']:
    coef_row_text.append([
            '$a_{' + col_des + ',1}$',
            '$a_{' + col_des + ',2}$',
            '$\cdot\cdot\cdot$',
            '$a_{' + col_des + ',N^{M}_{A}}$'
    ])
    topo_row_text.append([
            '$thr_{' + col_des + '}$',
            '$ChL_{' + col_des + '}$',
#             '$LfL_{' + col_des + '}$',
            '$ChR_{' + col_des + '}$',
#             '$LfR_{' + col_des + '}$',
            ]
    )

coef_row_text.insert(2, [
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  '',
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$"
])

topo_row_text.insert(2, [
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
#                   r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
#                   r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  ])

row_caption = [
    "Node 1",
    "Node 2",
    "",
    "Node $N^{M}_{n}(l)$"
]


coef_row = []
topo_row = []

pos = origin
for coef, topo, caption in zip(coef_row_text, topo_row_text, row_caption):
    if coef_row:
        pos = coef_row[-1][0].s(0)

    coef_row.append(make_row(pos, coef, field))
    topo_row.append(make_row(coef_row[-1][-1].e(0) + (7.5,0), topo, field))
    text(caption).align(coef_row[-1][0].w(0.5), prev().e(0.5))()

addr_dec = block("User Port Interface Controller", topo_row[0][-1].s(1.0) + (3,0) - coef_row[0][0].n()).over(coef_row[0][0], 5)()

stripe_line = []
stripe_line.append(path([coef_row[0][0].n() - (0, 4), coef_row[-1][0].s() + (0, 1)], dotted=True)())
stripe_text = ['32b Stripe',
            '$\cdot\cdot\cdot$',
               '$\cdot\cdot\cdot$',
               '$\cdot\cdot\cdot$',
               '32b Stripe',
               ]
stripe_line_span = (topo_row[0][-1].e() + (3,0) - coef_row[0][0].w())[0]/len(stripe_text)

for i in range(1, len(stripe_text)+1):
    stripe_line.append( path([stripe_line[i-1][0] + (stripe_line_span, 0), stripe_line[i-1][1] + (stripe_line_span, 0)], dotted=True)())
    text(stripe_text[i-1]).align_x(mid(stripe_line[i][0], stripe_line[i-1][0]), prev().c()).align_y(coef_row[0][0].n() - (0,1), prev().s())()
    bus([prev(1).c() - (0,1.2), palign(prev(1).c(), addr_dec.s())], style='<->', shorten=(0, 0.2))()

bus([addr_dec.e(0.5), addr_dec.e(0.5) + (3, 0)], style='<->', shorten = (0.2, 0))()
text("User Port").align(prev(1)[-1], prev().w(0.5))()

coef_brace = path([coef_row[-1][0].s() + (0, 0.5), coef_row[-1][-1].s(1.0) + (0, 0.5)], decorate=True, decoration='{brace,amplitude=10pt,mirror}')()
topo_brace = path([topo_row[-1][0].s() + (0, 0.5), topo_row[-1][-1].s(1.0) + (0, 0.5)], decorate=True, decoration='{brace,amplitude=10pt,mirror}')()

bus([coef_row[-1][2].s(0) + (0,1.5), coef_row[-1][2].s(0) + (0,3)], shorten = (0.2, 0.2), style='<->')()
cm_port_dec = block("CM Port Interface Controller", coef_row[0][-1].s(1.0) - coef_row[0][0].n()).align(coef_row[-1][2].s(0) + (0,3), prev().n(0.5))()

bus([topo_row[-1][1].s(0.5) + (0,1.5), topo_row[-1][1].s(0.5) + (0,3)], shorten = (0.2, 0.2), style='<->')()
sm_port_dec = block("SM Port Interface Controller", topo_row[0][-1].s(1.0) - topo_row[0][0].n()).align(topo_row[-1][1].s(0.5) + (0,3), prev().n(0.5))()

bus([cm_port_dec.w(0.5), cm_port_dec.w(0.5) - (6, 0)], style='<->', shorten = (0.2, 0))()
text("CM Port").align(prev(1)[-1], prev().e(0.5))()

bus([sm_port_dec.e(0.5), sm_port_dec.e(0.5) + (6, 0)], style='<->', shorten = (0.2, 0))()
text("SM Port").align(prev(1)[-1], prev().w(0.5))()

# addr_bus = bus([coef_brace.pos(0.5) + (-1,1.5), coef_row[-1][0].s(0.0) + (-2,4)], def_routing='|-', style='<-')()
# text("Coef Port").align(addr_bus[0] - (1,0), prev().e(0.5))()
# text("addr").align(addr_bus[-1], prev().e(0.5))()
# data_bus = bus([coef_brace.pos(0.5) + (1,1.5), coef_row[-1][0].s(0.0) + (-2,5)], def_routing='|-', style='->')()
# text("data").align(data_bus[-1], prev().e(0.5))()
# 
# addr_bus = bus([topo_brace.pos(0.5) + (1,1.5), topo_row[-1][-1].s(1.0) + (5,4)], def_routing='|-', style='<-')()
# text("Strct Port").align(addr_bus[0] + (1,0), prev().w(0.5))()
# text("addr").align(addr_bus[-1], prev().w(0.5))()
# data_bus = bus([topo_brace.pos(0.5) + (-1,1.5), topo_row[-1][-1].s(1.0) + (5,5)], def_routing='|-', style='->')()
# # text("Topo Port").align(addr_bus[0], prev().w(0.5))()
# text("data").align(data_bus[-1], prev().w(0.5))()
