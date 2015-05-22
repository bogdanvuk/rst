import json
import csv

import numpy as np
import scipy as sp
import scipy.stats

# naci confidence interval za svaki run crosvalidacije i staviti uz svaki mean

# naci confidence interval za niz speed-upa (za svaki dataset)

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, h

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
#         tmin = float('Inf')
#         tmax = 0
#         tavg = 0
#         runs = 0

        t = []
         
        for _,cv_run in r.items():
            for _,run in cv_run.items():
                t += [run['timing']]

        print(d)
        table[d][i] = mean_confidence_interval(t)

with open('results.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    csvwriter.writerow(['Dataset','HW/SW [s]','SW-ARM [s]','SW-PC [s]'])
    
    spdup_arm = []
    spdup_pc = []
    
    for d,res in iter(sorted(table.items())):
        row = [d]
        
        for r in res:
            row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(r[0], r[1])]
        
        spdup_arm += [res[1][0]/res[0][0]]
        spdup_pc += [res[2][0]/res[0][0]]
        
        csvwriter.writerow(row)
    
    row = ['Average speedup', '']
        
    row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(*mean_confidence_interval(spdup_arm))]
    row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(*mean_confidence_interval(spdup_pc))]
    
    csvwriter.writerow(row)
    
pass
