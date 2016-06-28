from bdp.node import *

bdp_config['grid'] = 8
text.font = 'footnotesize'
block.text_font = 'footnotesize'

# text("$\mathbf{a_{2}}\cdot \mathbf{A} < threshold_{2}$")()

node = block(size=p(2,2), shape='circle', node_sep=(2,2))
leaf = block(size=p(1.8,1.8), node_sep=(2,2))

def draw_children_con(parent, children):
    path([parent.c(), children[0].c()], shorten=(1.4, 1.4), style="->")()
    text("T").align(prev(1).c(), prev().s(1.0))()
     
    path([parent.c(), children[1].c()], shorten=(1.4, 1.4), style="->")()
    text("F").align(prev(1).c(), prev().s())()

def draw_children(parent, templ, t, separation):
    objs = []
    objs.append(templ[0](t[0]).below(parent).left(prev(), separation)())
    objs.append(templ[1](t[1]).below(parent).right(prev(), separation)())
    return objs

def draw_node_test_eq(node, id, pos):
    t = "$\mathbf{a_{" + str(id) + "}}\cdot \mathbf{A} < thr_{" + str(id) + "}$"
    if pos == 'left':
        text(t).align(node.w(0.5), prev().e(1.0))()
    else:
        text(t).align(node.e(0.5), prev().s())()
 
root = node("1")()
draw_node_test_eq(root, 1, 'right')

root_ch = draw_children(root, [node, node], ['2', '3'], 2)
draw_node_test_eq(root_ch[0], 2, 'left')
draw_node_test_eq(root_ch[1], 3, 'right')
draw_children_con(root, root_ch)

node2_ch = draw_children(root_ch[0], [node, leaf], ['4', '$C_{1}$'], 1)
draw_node_test_eq(node2_ch[0], 4, 'left')
draw_children_con(root_ch[0], node2_ch)

node3_ch = draw_children(root_ch[1], [leaf, node], ['$C_{2}$', '5'], 1)
draw_node_test_eq(node3_ch[1], 5, 'right')
draw_children_con(root_ch[1], node3_ch)

node4_ch = draw_children(node2_ch[0], [leaf, leaf], ['$C_{3}$', '$C_{4}$'], 1)
draw_children_con(node2_ch[0], node4_ch)

node5_ch = draw_children(node3_ch[1], [leaf, leaf], ['$C_{5}$', '$C_{6}$'], 1)
draw_children_con(node3_ch[1], node5_ch)

# path([root.s(), root_ch[0].s(), node2_ch[0].s(), node4_ch[1].n()], def_routing="edge[out=180,in=0,->]")()
# path([root.s(), root_ch[0].s(), node2_ch[0].s(1.0), node4_ch[1].w(0.5) - (1, 1), node4_ch[1].w(0.5)], smooth=True, thick=True, style='->')()
path([root.s(), root_ch[0].s(), node2_ch[0].c(), node4_ch[1].w(0.5)], rounded_corners=10, thick=True, shorten=(0.3, 0.5), style='->', draw='red')()
