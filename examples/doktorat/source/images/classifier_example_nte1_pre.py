from classifier_example_nte_tmpl import nte, ports, fig
from bdp import *

fig << '\definecolor{emphcolor}{RGB}{135,206,235}\n'
nte.text_t = "NTE$_1$"
nte['Coefficient*'].fill = 'emphcolor'
text_vals = text(margin=(0.3, 0.4))

for p in ['inst_inp_bus', 'cm_addr', 'cm_data']:
    ports[p].fill = 'emphcolor'

for p in ports['node_id_net']:
    ports['node_id_net'][p].fill = 'emphcolor'

for p in nte['mem_intf_net']:
    nte['mem_intf_net'][p].fill = 'emphcolor'

fig << text_vals(r"$\mathbf{x}=[41FF,19FF]$").aligny(ports['inst_inp_bus'][-1], cur().n()).alignx(nte.w())
fig << text_vals(r"$0$").aligny(ports['node_id_net'][0][0], cur().n()).alignx(nte.w())
fig << text_vals(r"$\mathbf{w}=[4D2A,81D1]$", margin=(-0.8, 1.2)).aligny(ports['cm_data'][-1], cur().n()).alignx(nte.w())
fig << text_vals(r"$0$").aligny(ports['cm_addr'][0], cur().n()).alignx(nte.w())

fig << ports
fig << nte

#render_fig(fig)
