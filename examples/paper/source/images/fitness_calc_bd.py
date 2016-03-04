from bdp.node import *

bus = path(double=True, thick=False)
bus_text = text(font="scriptsize", margin=p(0,0.2))

def create_fitness_border(pos, name):
    if name:
        bd = block(name, size=p(18,11), p=pos, text_margin=(0.5,0), text_font='small', text_align='nw', fill='white')()
    else:
        bd = block(name, size=p(18,11), p=pos, fill='white', dotted=True)()

def create_fitness_block(pos, name):
    bd = block(name, size=p(18,11), p=pos, text_margin=(0.5,0.5), text_font='small', text_align='nw', fill='white')()
    incr = block("Incrementer", size=p(7,3)).align(bd.n() + (1,2))()
    dc_calc = block("Dominant Class Calc.", size=p(7,3)).right(incr, 2)()
    mem = block(r"Class Distribution \\ Memory", size=p(10, 3)).align_y(incr.s() + (0, 2)).align_x(mid(incr.c(), dc_calc.c()), prev().c())()
    
    bus([incr.s(5), mem.n(2)], style='<->')()
    bus([dc_calc.s(2), mem.n(8)], style='<->')()
    
    return {'incr':incr,
            'mem':mem,
            'dc_calc':dc_calc,
            'bd':bd
            }
    

# create_fitness_border(origin, "Fitness Calculator for Leaf Node ID 1")
# create_fitness_border(origin + (1,1), "Fitness Calculator for Leaf Node ID 2")
# create_fitness_border(origin + (2,2), "")
fb = create_fitness_block(origin + (3,3), "Fitness Calculator for Leaf Node ID 1")
fbm = create_fitness_block(origin + (3,18), "Fitness Calculator for Leaf Node ID $N^{M}_{l}$")
text(r"$\cdot$ \\ $\cdot$ \\ $\cdot$", font="normalsize").align(mid(fb['bd'].c(), fbm['bd'].c()), prev().c())()
# for i in range(3):
#     text(r"$\cdot$ \\ $\cdot$ \\ $\cdot$", text_font='large').align_y(mid(fb1['bd'].c(), fb2['bd'].c()), prev().c()).align_x(fb1['bd'].n() + (2,0) + i*p(7,0))()



leaf_id_in = fb['incr'].w(1) - (8,0)
path([leaf_id_in, fb['incr'].w(1)], style='->')()
bus_text("$Leaf\ ID$").align(leaf_id_in, prev().s())()

class_in = fb['incr'].w(2) - (8,0)
path([class_in, fb['incr'].w(2)], style='->')()
bus_text("$C$").align(class_in, prev().s())()

path([fb['incr'].w(1) - (2,0), fbm['incr'].w(1)], def_routing='|-', style='->')()
path([fb['incr'].w(2) - (3,0), fbm['incr'].w(2)], def_routing='|-', style='->')()

acc_prov = block("Accuracy Provider", (6,16)).align(mid(fb['bd'].s(1.0), fbm['bd'].n(1.0)) + (11,-2), prev().w(0.5))()

# mux_block = block("MUX", (4,8)).align(mid(fb['bd'].s(1.0), fbm['bd'].n(1.0)) + (3,0), prev().w(0.5))()
# 
path([fb['dc_calc'].e(0.25), fb['dc_calc'].e(0.25) + (4,0), acc_prov.w(1)], style='->', def_routing='|-')()
bus_text("$dominant\\_class_1$").align(acc_prov.w(1) - (0.5, 0), prev().s(1.0))()
path([fb['dc_calc'].e(0.5), fb['dc_calc'].e(0.5) + (3,0), acc_prov.w(3)], style='->', def_routing='|-')()
bus_text("$dominant\\_class\\_cnt_{1}$").align(acc_prov.w(3) - (0.5, 0), prev().s(1.0))()
path([fb['dc_calc'].e(0.75), fb['dc_calc'].e(0.75) + (2,0), acc_prov.w(5)], style='->', def_routing='|-')()
bus_text("$total\_cnt_{1}$").align(acc_prov.w(5) - (0.5, 0), prev().s(1.0))()

path([fbm['dc_calc'].e(0.25), fbm['dc_calc'].e(0.25) + (2,0), acc_prov.w(11)], style='->', def_routing='|-')()
bus_text("$total\_cnt_{N^{M}_{l}}$").align(acc_prov.w(11) - (0.5, 0), prev().s(1.0))()
path([fbm['dc_calc'].e(0.5), fbm['dc_calc'].e(0.5) + (3,0), acc_prov.w(13)], style='->', def_routing='|-')()
bus_text("$dominant\\_class\\_cnt_{N^{M}_{l}}$").align(acc_prov.w(13) - (0.5, 0), prev().s(1.0))()
path([fbm['dc_calc'].e(0.75), fbm['dc_calc'].e(0.75) + (4,0), acc_prov.w(15)], style='->', def_routing='|-')()
bus_text("$dominant\\_class_{N^{M}_{l}}$").align(acc_prov.w(15) - (0.5, 0), prev().s(1.0))()


# path([fbm['dc_calc'].e(0.5), fbm['dc_calc'].e(0.5) + (2,0), mux_block.w(7)], style='->', def_routing='|-')()
text(r"$\cdot$ \\ $\cdot$ \\ $\cdot$", font="normalsize").align(acc_prov.w(0.5) - (2,0), prev().c())()
# 
# sum_block = block("Sum Block", size=(7,8), text_align='nw').right(mux_block, 2).align_y(mux_block.c(), prev().c())()
# 
# add_block = block("+", size=p(2,2), shape='circle')
# add = add_block.align(sum_block.w(0.5) + (2,0), prev().c())()
# reg = block(size=(2, 4)).right(add).align_y(add.c(), prev().c())()
# 
# path([mux_block.e(0.5), add.w(0.5)], style='->')()
# path([add.e(0.5), reg.w(0.5)], style='->')()
# path([reg.s(0.5), reg.s(0.5) + (0,1), add.s(0.5)], def_routing = '-|', style='->')()
# 
# # bus([fb['dc_calc'].e(0.5), add.w(0.5)], style='->', shorten=(0,0.3))()
# # 
path([acc_prov.e(5), acc_prov.e(5) + (6,0)], style='->')()
bus_text("hits").align(acc_prov.e(5) + (1,0), prev().s())()
bus([acc_prov.e(7), acc_prov.e(7) + (6,0)], style='->')()
bus_text("dt\\_classes").align(acc_prov.e(7) + (1,0), prev().s())()
bus([acc_prov.e(9), acc_prov.e(9) + (6,0)], style='->')()
bus_text("dt\\_impurity").align(acc_prov.e(9) + (1,0), prev().s())()
    


