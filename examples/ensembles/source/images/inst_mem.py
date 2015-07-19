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
        objs.append(tmpl(t, dotted=dotted)())
        
    
    
    return objs

row_text = [
            '$A_{1}$', 
            '$A_{2}$', 
            '$\cdot\cdot\cdot$',
            '$A_{N^{M}_{A}}$',
            '$C$',
            ]

blank_row_text = [
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  '',
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$"
                  ]

objs1 = make_row(origin, row_text,field)
text("Instance 1").align(objs1[0].w(0.5), prev().e(0.5))()
objs2 = make_row(objs1[0].s(), row_text,field)
text("Instance 2").align(objs2[0].w(0.5), prev().e(0.5))()
field.text_font = "tiny"
objs3 = make_row(objs2[0].s(), blank_row_text, field)
field.text_font = "small"
objs4 = make_row(objs3[0].s(), row_text, field)
text("Instance $N^{M}_{I}$").align(objs4[0].w(0.5), prev().e(0.5))()

addr_dec = block("Port A Address Decoder", objs1[-1].s(1.0) - objs1[0].n()).over(objs1[0], 5)()

stripe_line_span = (objs1[-1].e() - objs1[0].w())[0]/3  

stripe_text = ['32b Stripe',
               '$\cdot\cdot\cdot$',
               '32b Stripe',
               ]

stripe_line = []
stripe_headers = []
stripe_line.append(path([objs1[0].n() - (0, 4), objs4[0].s() + (0, 2)], dotted=True)())
for i in range(1, 4):
    stripe_line.append( path([stripe_line[i-1][0] + (stripe_line_span, 0), stripe_line[i-1][1] + (stripe_line_span, 0)], dotted=True)())
    stripe_headers.append(text(stripe_text[i-1]).align_x(mid(stripe_line[i][0], stripe_line[i-1][0]), prev().c()).align_y(objs1[0].n() - (0,1), prev().s())())
    bus([prev(1).c() - (0,1.2), palign(prev(1).c(), addr_dec.s())], style='<->')()

bus([addr_dec.e(0.5), addr_dec.e(0.5) + (3, 0)], style='<->')()
text("Port A").align(prev(1)[-1], prev().w(0.5))()

path([objs4[0].s() + (0, 1.5), objs4[-1].s(1.0) + (0, 1.5)], decorate=True, decoration='{brace,amplitude=10pt,mirror}')()
bus([objs4[2].s(0.5) + (0,3), objs4[-1].s(1.0) + (3,4)], def_routing='|-', style='->')()
text("Port B").align(prev(1)[-1], prev().w(0.5))()




# bus([stripe_headers[0].c() - (0,1.2), palign(stripe_headers[0].c(), addr_dec.s())], style='<-')()
