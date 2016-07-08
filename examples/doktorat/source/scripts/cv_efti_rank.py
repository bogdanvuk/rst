import os
import json
import csv
import numpy as np
import scipy as sp
import scipy.stats

algos = ['OC1-AP', 'OC1', 'CART-LC', 'OC1-SA', 'OC1-GA', 'OC1-ES', 'GALE', 'GaTree', 'HB-Lin', 'EFTI']

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, h


def load_js_data(fname):
    with open(fname) as data_file:
        res = json.load(data_file)

    return res

def combine_efti_data(data, efti_res, attr_name, factor):
    for r in efti_res['pc_run']:
        ds = r['dataset']
        if 'EFTI' not in data[attr_name][ds]:
            data[attr_name][ds]['EFTI'] = []
            
        data[attr_name][ds]['EFTI'].append(r[attr_name]*factor)

def load_other_algo_data(cv_other_dir):
    data = {}
    for cv_other_fn, attr_name in zip(['cv_data_acc.js', 'cv_data_size.js'], ['accuracy', 'leaves']):
        data[attr_name] = load_js_data(os.path.join(cv_other_dir, cv_other_fn))

    return data

def load_cv_data(cv_other_dir, efti_cvjs):
    data = load_other_algo_data(cv_other_dir)
    efti_res = load_js_data(efti_cvjs)
    
    for attr_name, factor in zip(['accuracy', 'leaves'], [100, 1]):
        combine_efti_data(data, efti_res, attr_name, factor)

    return data

efti_cvjs = 'cv_20160708_131037_pc_impurity.js'
results_acc_csv = 'cv_20160708_131037_pc_impurity_acc.csv'
results_size_csv = 'cv_20160708_131037_pc_impurity_size.csv'
cv_other_dir = '/home/bvukobratovic/projects/rst/examples/doktorat/source/scripts/'
data = load_cv_data(cv_other_dir, efti_cvjs)

acc_table = {}
size_table = {}
for ds in data['accuracy']:
    acc_table[ds] = {}
    size_table[ds] = {}
    for algo in algos:
        acc_table[ds][algo] = mean_confidence_interval(data['accuracy'][ds][algo])
        size_table[ds][algo] = mean_confidence_interval(data['leaves'][ds][algo])

for fn, table in zip([results_acc_csv, results_size_csv], [acc_table, size_table]):
    with open(fn, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        csvwriter.writerow(['Dataset'] + algos)
    
        for d,res in iter(sorted(table.items())):
            row = [d]
        
            for a in algos:
                #row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(res[a][0], res[a][1])]
                row += ["{0:0.2f}±{1:0.2f}".format(res[a][0], res[a][1])]
               
            csvwriter.writerow(row)
        
    # row = ['Average speedup', '']
    
    # row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(*mean_confidence_interval(spdup_arm))]
    # row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(*mean_confidence_interval(spdup_pc))]
    # row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(*mean_confidence_interval(spdup_dsp))]
    
        #csvwriter.writerow(row)
