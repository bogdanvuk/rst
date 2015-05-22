import json
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

arm_js = '/data/projects/rst/examples/paper/source/data/crossvalidation/arm.js'
hw_js = '/data/projects/rst/examples/paper/source/data/crossvalidation/hw.js'
pc_js = '/data/projects/rst/examples/paper/source/data/crossvalidation/pc.js'

with open(arm_js) as f:    
    arm_res = json.load(f)
with open(hw_js) as f:    
    hw_res = json.load(f)
with open(pc_js) as f:    
    pc_res = json.load(f)

table = {}    

for d in hw_res['dataset']:
    table[d] = [(), (), ()]
    
for i, res in enumerate([hw_res, arm_res, pc_res]):
    for d, r in res['res'].items():

        t = []
         
        for _,cv_run in r.items():
            for _,run in cv_run.items():
                t += [run['timing']]

        table[d][i] = sum(t)/len(t)

spdup_arm = []
spdup_pc = []
datasets = []
        
for d,res in iter(sorted(table.items())):
    spdup_arm += [res[1]/res[0]]
    spdup_pc += [res[2]/res[0]]
    datasets += [d]

fs = 20

fig, (ax0, ax1) = plt.subplots(figsize=(16,6), nrows=2, sharex=True, tight_layout=True)

ax0.scatter(range(len(datasets)), spdup_arm, s=50)
ax0.yaxis.set_major_locator(MultipleLocator(20))
ax0.set_title('a) HW/SW speedup over SW-ARM implementation', fontsize=fs, loc='left')
ax1.scatter(range(len(datasets)), spdup_pc, s=50)
ax1.set_title('b) HW/SW speedup over SW-PC implementation', fontsize=fs, loc='left')
plt.xticks(range(len(datasets)), datasets)
plt.margins(0.03)
plt.tick_params(axis='both', which='major', labelsize=18)

plt.show()