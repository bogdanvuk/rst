from bdp.node import *

field = block(size=p(6,3))

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
            '$a_{1}$', 
            '$a_{2}$', 
            '$\cdot\cdot\cdot$',
            '$a_{N^{M}_{A}}$',
            '$threshold$',
            'Child Left ID',
            'Leaf Left ID',
            'Child Right ID',
            'Leaf Right ID',
            ]

blank_row_text = [
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  '',
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$",
                  r"$\cdot$ \\ $\cdot$ \\ $\cdot$"
                  ]

objs1 = make_row(origin, row_text,field)
text("Node 1").align(objs1[0].w(0.5), prev().e(0.5))()
objs2 = make_row(objs1[0].s(), row_text,field)
text("Node 2").align(objs2[0].w(0.5), prev().e(0.5))()
field.text_font = "tiny"
objs3 = make_row(objs2[0].s(), blank_row_text, field)
field.text_font = "small"
objs4 = make_row(objs3[0].s(), row_text, field)
text("Node $N^{M}_{nl}$").align(objs4[0].w(0.5), prev().e(0.5))()

stripe_line = []
stripe_line.append(path([objs1[0].n() - (0, 4), objs4[0].s() + (0, 2)], dotted=True)())
stripe_text = ['32b Stripe',
               '$\cdot\cdot\cdot$',
               '$\cdot\cdot\cdot$',
               '32b Stripe',
               ]
stripe_line_span = (objs1[-1].e() - objs1[0].w())[0]/len(stripe_text) 

for i in range(1, len(stripe_text)+1):
    stripe_line.append( path([stripe_line[i-1][0] + (stripe_line_span, 0), stripe_line[i-1][1] + (stripe_line_span, 0)], dotted=True)())
    text(stripe_text[i-1]).align_x(mid(stripe_line[i][0], stripe_line[i-1][0]), prev().c()).align_y(objs1[0].n() - (0,1), prev().s())()
    
    