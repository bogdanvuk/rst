from bdp.node import *

# mul_block = block("x", size=p(2,2), shape='circle')()
# path([mul_block.n(0.25), mul_block.n(0.25) - (1,1)])()
# mul_block = block(size=p(2,2))()
# path([mul_block.n(0.25), mul_block.n(0.25) + (0,5)])()



mul_block = block("x", size=p(2,2), shape='circle')
add_block = block("+", size=p(2,2), shape='circle')
 
mul = []

inp_coef_tmpl = block(size=p(2,2), border=False)

inp_coefs = []

inp_coefs.append(inp_coef_tmpl("$A_{1}$")())
inp_coefs.append(inp_coef_tmpl("$a_{1}$").below(prev(1))())
inp_coefs.append(inp_coef_tmpl("$A_{2}$").below(prev(1), 2)())
inp_coefs.append(inp_coef_tmpl("$a_{2}$").below(prev(1))())
 
for i in range(len(inp_coefs)):
    mul.append(mul_block.right(inp_coefs[i])())
    path([inp_coefs[2*i].c(), mul[i].c()], shorten=(1.5, 1.5), style='->', thick=True)()
    path([inp_coefs[i+1].c(), mul[i].c()], shorten=(1.5, 1.5), style='->', thick=True)()
 
add = []
 
for i in range(2):
    add.append(add_block.align_y(mid(mul[2*i].p, mul[2*i+1].p)).align_x(mul[2*i].n() + (6, 0))())
    path([mul[2*i].c(), add[i].c()], shorten=(1.5, 1.5), style='->', thick=True)()
    path([mul[2*i+1].c(), add[i].c()], shorten=(1.5, 1.5), style='->', thick=True)()
 
add.append(add_block.align_y(mid(add[0].p, add[1].p)).align_x(add[0].n() + (8, 0))())
for i in range(2):
    path([add[i].c(), add[2].c()], shorten=(1.5, 1.5), style='->', thick=True)()

 
