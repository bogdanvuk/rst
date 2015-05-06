from os import listdir, path
from os.path import isfile, join
import matplotlib.pyplot as plt
import csv
import pylab
import os

# print("[BLA] " + os.getcwd())

# gmon_csv_path = os.getcwd() + '\glupost'

#gmon_csv_path = '/home/bvukobratovic/projects/rst/examples/paper/source/data/profiling'
gmon_csv_path = '../data/profiling'

files = sorted([ f for f in listdir(gmon_csv_path) 
                if isfile(join(gmon_csv_path,f)) and path.splitext(f)[1] == '.csv' ], key=str.lower)


datasets = []
percents = []

for f in files:
    
    with open(join(gmon_csv_path,f), 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        
        fit_eval_perc = 0
        
        for row in spamreader:
            if row[0] in ['evaluate_node_test', 'find_dt_leaf_for_inst', 'find_node_distribution', 'fitness_eval']:
                fit_eval_perc += float(row[3])
                
        datasets.append(path.splitext(f)[0].split('_')[1])
        percents.append(fit_eval_perc)

fig = plt.figure(figsize=(16,4), tight_layout=True)
plt.plot(range(len(datasets)), percents)
plt.xticks(range(len(datasets)), datasets)
plt.margins(0.03)
# fig.tight_layout()
plt.show()