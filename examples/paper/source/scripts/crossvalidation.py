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
dsp_js = '/data/projects/rst/examples/paper/source/data/crossvalidation/dsp.js'
hw_js = '/data/projects/rst/examples/paper/source/data/crossvalidation/hw.js'
pc_js = '/data/projects/rst/examples/paper/source/data/crossvalidation/pc.js'

with open(arm_js) as f:    
    arm_res = json.load(f)
with open(dsp_js) as f:    
    dsp_res = json.load(f)    
with open(hw_js) as f:    
    hw_res = json.load(f)
with open(pc_js) as f:    
    pc_res = json.load(f)

table = {}    

for d in hw_res['dataset']:
    table[d] = [(), (), (), ()]

hw_run = []
if 'hw_run' in hw_res:
    hw_run.extend(hw_res['hw_run'])

pc_run = []  
arm_run = []
dsp_run = []

for s, res, run in zip(['pc_run', 'arm_run', 'dsp_run'], [pc_res, arm_res, dsp_res], [pc_run, arm_run, dsp_run]):
    if s in res:
        run.extend(res[s])

dsp_run = []
if 'dsp_run' in dsp_res:
    dsp_run.extend(dsp_res['dsp_run'])

dsp_run = []
if 'dsp_run' in dsp_res:
    dsp_run.extend(dsp_res['dsp_run'])


hw_times = {}
for run in hw_run:
    dataset_name = run['dataset']
    if dataset_name not in hw_times:
        hw_times[dataset_name] = []
    
    hw_times[dataset_name].append(run['timing'])

for d, t in hw_times.items():
    table[d][0] = mean_confidence_interval(t)
    
dsp_times = {}
pc_times = {}
arm_times = {}
for i,(timings, run_list) in enumerate(zip([arm_times, pc_times , dsp_times],[arm_run, pc_run, dsp_run])):
    for run in run_list:
        dataset_name = run['dataset']
        if dataset_name not in timings:
            timings[dataset_name] = []
            
        timings[dataset_name].append(run['timing'])

    for d, t in timings.items():
        table[d][i+1] = mean_confidence_interval(t)

with open('results.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    csvwriter.writerow(['Dataset','HW/SW [s]','SW-ARM [s]','SW-PC [s]','SW-DSP [s]'])
    
    spdup_arm = []
    spdup_dsp = []
    spdup_pc = []
    
    for d,res in iter(sorted(table.items())):
        row = [d]
        
        for r in res:
            try:
                row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(r[0], r[1])]
            except:
                row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(0, 0)]
        
        spdup_arm += [res[1][0]/res[0][0]]
        spdup_pc += [res[2][0]/res[0][0]]
        try:
            spdup_dsp += [res[3][0]/res[0][0]]
        except:
            pass
        
        csvwriter.writerow(row)
    
    row = ['Average speedup', '']
        
    row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(*mean_confidence_interval(spdup_arm))]
    row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(*mean_confidence_interval(spdup_pc))]
    row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(*mean_confidence_interval(spdup_dsp))]
    
    csvwriter.writerow(row)
    
pass
