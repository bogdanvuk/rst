from subprocess import Popen, PIPE
from cv_server import SerialCmd
#from multicomp_rank import multicomp_rank
import time
import json
import pexpect
import os
import sys


def crossvalidation(fname):
    with SerialCmd(fname) as ser_cmd:
        p = pexpect.spawnu(efti_app, echo=True, timeout=300)

        try:
            while (1):
                p.expect('\n')
                print(p.before)
                ser_cmd.cmd_decode(p.before + '\n')
        except pexpect.EOF:
            pass

def load_js_data(fname):
    with open(fname) as data_file:
        res = json.load(data_file)

    return res

def rank(data, desc=False):
    ranks = {}
    for ds in sorted(data.keys()):
        #if ds not in ['w40', 'vow']:
        #if ds not in ['gls', 'ion', 'page', 'son', 'veh', 'vow', 'w40', 'zoo']:
        ranks[ds] = multicomp_rank(data[ds], desc=desc)

    return ranks

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

def create_rank_table(data, desc, rankjs):

    algo_rank = {}
    avg = {}
    for attr_name, d in zip(data.keys(), desc):
        algo_rank[attr_name] = rank(data[attr_name], d)
#    print(algo_rank)

        combined = {}

        for n, d in algo_rank[attr_name].items():
            print(n, ': ', d)
            for a, r in d.items():
                if a not in combined:
                    combined[a] = []

                combined[a].append(r);

        avg[attr_name] = {}
        for a in combined:
            avg[attr_name][a] = sum(combined[a])/len(combined[a])


        print(sorted(avg[attr_name].items(), key=lambda x: x[1]))

    with open(rankjs, 'w') as outfile:
        json.dump({'rank': algo_rank, 'avg': avg}, outfile)

categ_max = {'ausc': 2,'bc': 3,'bcw': 2,'ger': 2,'gls': 7,'hep': 2,'hrts': 2,'ion': 2,'irs': 3,'liv': 2,'lym': 4,'page': 5,'pid': 2,'son': 2,'thy': 4,'veh': 4,'vote': 2,'vow': 11,'w40': 3,'zoo': 7}

def calc_data_fitness(data, complexity_weight=0.05):
    fit_data = {}
    for ds in data['accuracy']:
        fit_data[ds] = {}
        for algo in data['accuracy'][ds]:
            fit_data[ds][algo] = []
            for acc, leaves in zip(data['accuracy'][ds][algo], data['leaves'][ds][algo]):
                fit_data[ds][algo].append(acc * (complexity_weight*(categ_max[ds] - leaves)/categ_max[ds] + 1));

    return {'fit': fit_data}

if __name__ == "__main__":

   efti_app = '/home/projects/efti/Release/efti ' + ' '.join(sys.argv[1:])

   efti_cvjs = "cv_{0}_pc_impurity.js".format(time.strftime("%Y%m%d_%H%M%S"))
   rankjs = "cv_{0}_pc_impurity_rank.js".format(time.strftime("%Y%m%d_%H%M%S"))
   cv_other_dir = '.'
   #efti_cvjs = 'cv_20160708_161726_pc_impurity.js'
   #rankjs = 'cv_20160708_161726_pc_impurity_rank.js'

   crossvalidation(efti_cvjs)
#data = load_cv_data(cv_other_dir, efti_cvjs)

#fit_data = calc_data_fitness(data)
#create_rank_table(fit_data, [True], rankjs)

#create_rank_table(data, [True, False], rankjs)

#
