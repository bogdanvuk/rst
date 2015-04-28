from bdp.node import *

bus = path(double=True, thick=False)
bus_text = text(font="scriptsize", margin=p(0,0))

def create_fitness_border(pos, name):
    if name:
        bd = block(name, size=p(18,11), p=pos, text_margin=(0.5,0), text_font='scriptsize', text_align='nw', fill='white')()
    else:
        bd = block(name, size=p(18,11), p=pos, fill='white', dotted=True)()

def create_fitness_block(pos, name):
    bd = block(name, size=p(18,11), p=pos, text_margin=(0.5,0), text_font='scriptsize', text_align='nw', fill='white')()
    incr = block("Incrementer", size=p(7,3)).align(bd.n() + (1,2))()
    dc_calc = block("Dominant Class Calc.", size=p(7,3)).right(incr, 2)()
    mem = block("Memory", size=p(10, 3)).align_y(incr.s() + (0, 2)).align_x(mid(incr.c(), dc_calc.c()), prev().c())()
    
    bus([incr.s(5), mem.n(2)], style='<->')()
    bus([dc_calc.s(2), mem.n(8)], style='<->')()
    
    return {'incr':incr,
            'mem':mem,
            'dc_calc':dc_calc,
            'bd':bd
            }
    

create_fitness_border(origin, "Fitness Calculator for Leaf Node ID 1")
create_fitness_border(origin + (1,1), "Fitness Calculator for Leaf Node ID 2")
create_fitness_border(origin + (2,2), "")
fb = create_fitness_block(origin + (3,3), "Fitness Calculator for Leaf Node ID $N^{M}_{l}$")
# for i in range(3):
#     text(r"$\cdot$ \\ $\cdot$ \\ $\cdot$", text_font='large').align_y(mid(fb1['bd'].c(), fb2['bd'].c()), prev().c()).align_x(fb1['bd'].n() + (2,0) + i*p(7,0))()


leaf_id_in = fb['incr'].w(1) - (8,0)
path([leaf_id_in, fb['incr'].w(1)], style='->')()
bus_text("$Leaf\ ID$").align(leaf_id_in, prev().s())()

class_in = fb['incr'].w(2) - (8,0)
path([class_in, fb['incr'].w(2)], style='->')()
bus_text("$C$").align(class_in, prev().s())()

add_block = block("+", size=p(2,2), shape='circle')

add = add_block.right(fb['dc_calc'], 3).align_y(fb['dc_calc'].c(), prev().c())()

bus([fb['dc_calc'].e(0.5), add.w(0.5)], style='->', shorten=(0,0.3))()

path([add.e(0.5), add.e(0.5) + (2,0)], shorten=(0.3, 0), style='->')()
bus_text("hits").align(add.e(0.5), prev().s())()
# 
# path([class_in, fb1['incr'].w(2)], style='->')()
# path([class_node, fb2['incr'].w(2)], def_routing='|-', style='->')()
# path([class_node, mid(fb1['bd'].s(), fb2['bd'].n()) + (1, 1)], def_routing='|-', style='->', dotted=True)()
# 
# 
#     
# path([fb1['incr'].w(2) - (5,0), fb1['incr'].w(2)], style='->')()