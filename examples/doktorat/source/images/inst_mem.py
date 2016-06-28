from bdp.node import *

field = block(size=p(6,2))
bus = path(double=True, thick=False)

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
for col_des in ['1', '2', 'N^{M}_{I}']:
    coef_row_text.append([
            '$A_{' + col_des + ',1}$',
            '$A_{' + col_des + ',2}$',
            '$\cdot\cdot\cdot$',
            '$A_{' + col_des + ',N^{M}_{A}}$',
            '$C_{' + col_des + '}$'
    ])
    
coef_row_text.insert(2, [
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  '',
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$"
])

row_caption = [
    "Instance 1",
    "Instance 2",
    "",
    "Instance $N^{M}_{I}$"
]


coef_row = []

pos = origin
for coef, caption in zip(coef_row_text, row_caption):
    if coef_row:
        pos = coef_row[-1][0].s(0)

    coef_row.append(make_row(pos, coef, field))
    text(caption).align(coef_row[-1][0].w(0.5), prev().e(0.5))()

addr_dec = block("User Port Interface Controller", coef_row[0][-1].s(1.0) - coef_row[0][0].n()).over(coef_row[0][0], 5)()

stripe_line_span = (coef_row[0][-1].e() - coef_row[0][0].w())[0]/3  
 
stripe_text = ['32b Stripe',
               '$\cdot\cdot\cdot$',
               '32b Stripe',
               ]
 
stripe_line = []
stripe_headers = []
stripe_line.append(path([coef_row[0][0].n() - (0, 4), coef_row[-1][0].s() + (0, 1)], dotted=True)())
for i in range(1, 4):
    stripe_line.append( path([stripe_line[i-1][0] + (stripe_line_span, 0), stripe_line[i-1][1] + (stripe_line_span, 0)], dotted=True)())
    stripe_headers.append(text(stripe_text[i-1]).align_x(mid(stripe_line[i][0], stripe_line[i-1][0]), prev().c()).align_y(coef_row[0][0].n() - (0,1), prev().s())())
    bus([prev(1).c() - (0,1.2), palign(prev(1).c(), addr_dec.s())], style='<->', shorten=(0.2, 0))()

bus([coef_row[-1][2].s(0.5) + (0,1.5), coef_row[-1][2].s(0.5) + (0,3)], shorten = (0.2, 0.2), style='<->')()
nte_port_dec = block("NTE Port Interface Controller", coef_row[0][-1].s(1.0) - coef_row[0][0].n()).align(coef_row[-1][2].s(0.5) + (0,3), prev().n(0.5))()

bus([addr_dec.e(0.5), addr_dec.e(0.5) + (3, 0)], style='<->')()
text("User Port").align(prev(1)[-1], prev().w(0.5))()

bus([nte_port_dec.e(0.5), nte_port_dec.e(0.5) + (3, 0)], style='<->')()
text("NTE Port").align(prev(1)[-1], prev().w(0.5))()

 
path([coef_row[-1][0].s() + (0, 0.5), coef_row[-1][-1].s(1.0) + (0, 0.5)], decorate=True, decoration='{brace,amplitude=10pt,mirror}')()
# bus([coef_row[-1][2].s(0.5) + (0,3), coef_row[-1][-1].s(1.0) + (3,4)], def_routing='|-', style='->')()
# text("NTE Port").align(prev(1)[-1], prev().w(0.5))()




# bus([stripe_headers[0].c() - (0,1.2), palign(stripe_headers[0].c(), addr_dec.s())], style='<-')()
