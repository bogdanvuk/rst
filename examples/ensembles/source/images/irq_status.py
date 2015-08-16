from bdp import *

bit = block(size=(6,4), fill='white')

fig << block(size=(30, 4), fill='white')
fig << block(size=(30, 4), dashed=True, fill='white').align(fig[-1].n(-1,-1))

fig << bit("SMAE 31 Status Bit").align(fig[-1].n(-1,-1))
fig << bit("SMAE 30 Status Bit").right(fig[-1], 0)
fig << bit(". . .").right(fig[-1], 0)
fig << bit("SMAE 1 Status Bit").right(fig[-1], 0)
fig << bit("SMAE 0 Status Bit").right(fig[-1], 0)
