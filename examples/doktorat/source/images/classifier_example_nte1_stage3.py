from bdp import *
from classifier_example_nte_tmpl import nte, ports, fig, bus_text
import copy
nte = copy.deepcopy(nte)
ports = copy.deepcopy(ports)

fig << '\definecolor{emphcolor}{RGB}{135,206,235}\n'
nte.text_t = "NTE$_1$"

for b in [r"$\geq$", 'MUX1', 'MUX2']:
    nte[b].fill = 'emphcolor'

nte['Instance Queue'][2].fill = 'emphcolor'
nte['Instance Queue'][2].text_t = r"$\mathbf{x}=[41FF,19FF]$"
nte['Node Queue'][2].fill = 'emphcolor'
nte['Node Queue'][2].text_t = '0'
text_vals = text(margin=(0.3, 0.4))

# for g in ['add0']:
#     for e in nte[g]:
#         nte[g][e].fill = 'emphcolor'

for b in ['final_add_reg_bus', 'thr_reg_bus', 'chl_reg_bus', 'chr_reg_bus', 'node_id_mux', 'mux1_res_bus']:
    nte[b].fill = 'emphcolor'

for b in ['inst_out', 'node_id_out']:
    ports[b].fill = 'emphcolor'

fig << text_vals(r"$2113$").align(nte[r"$\geq$"].w(1) - p(1.5,0), cur().s(1.0))
fig << text_vals(r"$FA20$").align(nte[r"$\geq$"].w(2) - p(1.5,0), cur().n(1.0))

fig << text_vals("1").align(nte['MUX1'].s(1), cur().n(1.1, -0.2))
fig << text_vals("0").align(nte['MUX1'].s(2), cur().n(-0.1, -0.2))
fig << text_vals("True").align(nte[r"$\geq$"].n(0.5), cur().s(0.5))
fig << text_vals("1").align(nte[r"$\geq$"].e(0.5), cur().s())

fig << text_vals("0").align(nte['msb_path'][0], cur().n())
fig << text_vals("0").align(nte['MUX2'].e(0.5), cur().s())

fig << text_vals("0").align(nte['MUX2'].s(1), cur().n(1.1, -0.2))
fig << text_vals("0").align(nte['MUX2'].s(2), cur().n(-0.1, -0.2))


fig << ports
fig << nte

#render_fig(fig)
