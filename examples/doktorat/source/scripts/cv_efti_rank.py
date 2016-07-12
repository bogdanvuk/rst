import os
import json
import csv
import numpy as np
import scipy as sp
import scipy.stats

algos = ['OC1-AP', 'OC1', 'CART-LC', 'OC1-SA', 'OC1-GA', 'OC1-ES', 'GALE', 'GaTree', 'HB-Lin', 'EFTI']
categ_max = {'ausc': 2,'bc': 3,'bcw': 2, 'ca':2,'car':4, 'cmc': 3, 'ctg':10, 'ger': 2,'gls': 7,'hep': 2,'hrts': 2,'ion': 2,'irs': 3,'jvow':9,'liv': 2,'lym': 4,'page': 5,'pid': 2,'psd':2,'sb':2,'seg':7,'sick':2,'son': 2,'spect':2, 'spf':7, 'thy': 4,'ttt':2,'veh': 4,'vote': 2,'vow': 11,'w21':3,'w40': 3,'wine':3,'wfr':4,'zoo': 7}

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

def form_csv_table(fn, table, algos):
    with open(fn, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csvwriter.writerow(['Dataset'] + algos)

        for d,res in iter(sorted(table.items())):
            row = [d]

            for a in algos:
                #row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(res[a][0], res[a][1])]
                #row += ["{0:0.2f}±{1:0.2f}".format(res[a][0], res[a][1])]
                row += ["{0:0.2f}".format(res[a][0])]

            csvwriter.writerow(row)

        # row = ['Average speedup', '']

        # row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(*mean_confidence_interval(spdup_arm))]
        # row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(*mean_confidence_interval(spdup_pc))]
        # row += [":math:`{0:0.1f} \pm {1:0.2f}`".format(*mean_confidence_interval(spdup_dsp))]

            #csvwriter.writerow(row)

def efti_with_others():
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
        form_csv_table(fn, table, algos)

def combine_efti_data(data, efti_res, attr_name, factor):
    for r in efti_res['pc_run']:
        ds = r['dataset']
        if 'EFTI' not in data[attr_name][ds]:
            data[attr_name][ds]['EFTI'] = []

        data[attr_name][ds]['EFTI'].append(r[attr_name]*factor)

def calc_data_fitness(data, complexity_weight=0.2):
    fit_data = {}
    for ds in data['accuracy']:
        fit_data[ds] = {}
        for algo in range(len(data['accuracy'][ds])):
            fit_data[ds][algo] = []
            for acc, leaves in zip(data['accuracy'][ds][algo], data['size'][ds][algo]):
                fit_data[ds][algo].append(acc * (complexity_weight*(categ_max[ds] - leaves)/categ_max[ds] + 1));

    return {'fit': fit_data}

def inter_efti():
    efti_cvjs = [
        'cv_20160712_113645_pc_impurity.js',
        'cv_20160712_113805_pc_impurity.js',
        'cv_20160712_113832_pc_impurity.js',
        'cv_20160712_143018_pc_impurity.js',
        'cv_20160712_143101_pc_impurity.js',
        'cv_20160712_143220_pc_impurity.js',
        'cv_20160709_153106_pc_impurity.js',
        'cv_20160709_153150_pc_impurity.js',
        'cv_20160709_153152_pc_impurity.js',
        'cv_20160709_153155_pc_impurity.js',
        'cv_20160711_231443_pc_impurity.js',
        'cv_20160711_231457_pc_impurity.js',
        'cv_20160711_231509_pc_impurity.js',
        'cv_20160711_231519_pc_impurity.js'
    ]

    data = {'accuracy': {}, 'size': {}}
    for i, e in enumerate(efti_cvjs):
        efti_res = load_js_data(e)
        for r in efti_res['pc_run']:
            ds = r['dataset']

            if ds not in data['accuracy']:
                data['accuracy'][ds] = []
                data['size'][ds] = []

            if i not in data['accuracy'][ds]:
                data['accuracy'][ds].extend([[] for _ in range(1 + i - len(data['accuracy'][ds]))])
                data['size'][ds].extend([[] for _ in range(1 + i - len(data['size'][ds]))])

            data['size'][ds][i].append(r['leaves'])
            data['accuracy'][ds][i].append(r['accuracy'])


    fit = calc_data_fitness(data, complexity_weight=0.2)

    acc_table = {}
    size_table = {}
    fit_table = {}
    for ds in data['accuracy']:
        acc_table[ds] = {}
        size_table[ds] = {}
        fit_table[ds] = {}
        for algo in range(len(efti_cvjs)):
            if data['accuracy'][ds][algo]:
                acc_table[ds][algo] = mean_confidence_interval(data['accuracy'][ds][algo])
                size_table[ds][algo] = mean_confidence_interval(data['size'][ds][algo])
                fit_table[ds][algo] = mean_confidence_interval(fit['fit'][ds][algo])
            else:
                acc_table[ds][algo] = (0,0)
                size_table[ds][algo] = (0,0)
                fit_table[ds][algo] = (0,0)

    results_acc_csv = 'efti_compare_acc.csv'
    results_size_csv = 'efti_compare_size.csv'
    results_fit_csv = 'efti_compare_fit.csv'
    for fn, table in zip([results_acc_csv, results_size_csv, results_fit_csv], [acc_table, size_table, fit_table]):
        form_csv_table(fn, table, list(range(len(efti_cvjs))))

inter_efti()
