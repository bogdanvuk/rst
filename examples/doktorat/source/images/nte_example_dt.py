from eftirun_findt import dt
from dtdtools import draw_dt, templdef
from bdp import *

bus_cap = cap(length=0.4, width=0.6, inset=0, type='Stealth')
bus = path(style=(bus_cap, bus_cap), line_width=0.3, double=True, border_width=0.06)
lvl_path = path(dotted=True)

templdef['node'].nodesep = (0.3, 2)
root = draw_dt(dt)

fig << root

def coef2hex(val):
    return '{:04X}'.format(int(val) & (2**16-1))

def draw_coeffs(node, bdp_node, pos='right'):
    if node['c']:
        w = [coef2hex(w*32768) for w in node['w']]
        w.append(coef2hex(node['thr']*32768/(1 << 1)))
        t = r"$w = [{}, {}], \theta={}$".format(*w)
        print(t)
        fig << getattr(text(t), pos)(bdp_node)
        draw_coeffs(node['c'][0], bdp_node['left'], 'left')
        draw_coeffs(node['c'][1], bdp_node['right'], 'right')

draw_coeffs(dt, root)

render_fig(fig)
