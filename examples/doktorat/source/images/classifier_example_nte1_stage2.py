from bdp import *
from classifier_example_nte_tmpl import nte, ports, fig, bus_text
import copy
nte = copy.deepcopy(nte)
ports = copy.deepcopy(ports)

fig << '\definecolor{emphcolor}{RGB}{135,206,235}\n'
nte.text_t = "NTE$_1$"
nte['Structural*'].fill = 'emphcolor'
nte['Instance Queue'][1].fill = 'emphcolor'
nte['Instance Queue'][1].text_t = r"$\mathbf{x}=[41FF,19FF]$"
nte['Node Queue'][1].fill = 'emphcolor'
nte['Node Queue'][1].text_t = '0'
text_vals = text(margin=(0.3, 0.4))

for g in ['add0']:
    for e in nte[g]:
        nte[g][e].fill = 'emphcolor'

for p in ['node_id_sm_bus', 'chr_bus', 'chl_bus', 'thr_bus']:
    nte[p].fill = 'emphcolor'

for p in ['sm_addr', 'sm_data']:
    ports[p].fill = 'emphcolor'

nte[r"$\theta$"] = bus_text(r"$\theta = FA20$").align(nte[r"$\theta$"].p)
nte[r"$ChL$"] = bus_text(r"$ChL = 0$").align(nte[r"$ChL$"].p)
nte[r"$ChR$"] = bus_text(r"$ChR = 1$").align(nte[r"$ChR$"].p)

fig << text_vals(r"$13E486D6$").align(nte['mul'][0].n(1.0), cur().s())
fig << text_vals(r"$0D2EB82F$").align(nte['mul'][1].s(1.0), cur().n())
fig << text_vals(r"$21133F05$").align(nte['add0'][0].n(0.7), cur().s())

# fig << text_vals(r"$4D2A$").align(nte['inp_coefs'][0].n(0.5) + p(0, 0.7), cur().s(0.5))
# fig << text_vals(r"$41FF$").align(nte['inp_coefs'][1].n(0.5) + p(0, 0.7), cur().s(0.5))
# fig << text_vals(r"$81D1$").align(nte['inp_coefs'][2].n(0.5) + p(0, 0.7), cur().s(0.5))
# fig << text_vals(r"$19FF$").align(nte['inp_coefs'][3].n(0.5) + p(0, 0.7), cur().s(0.5))

fig << ports
fig << nte

render_fig(fig)
