import os
import scipy.io
from itertools import chain

algos = ['OC1-AP', 'OC1', 'CART-LC', 'OC1-SA', 'OC1-GA', 'OC1-ES', 'GALE', 'GaTree', 'HB-Lin']

di = list(chain(range(4,10), range(11,12), range(13, 15), range(16, 20), range(21, 22), range(27, 28), range(30,31), range(32,35), range(36,37)))

accronyms = {'australian': 'ausc', 
             'thyroid': 'thy',
             'lymphography': 'lym',
             'pima_indians_diabetes': 'pid',
             'waveform40': 'w40',
             'glass': 'gls',
             'ionosphere': 'ion',
             'iris': 'irs',
             'vote': 'vote',
             'vehicle': 'veh',
             'page_blocks': 'page',
             'liver': 'liv',
             'heart_statlog': 'hrts',
             'german': 'ger',
             'sonar': 'son',
             'vowel': 'vow',
             'breast_cancer': 'bc',
             'hepatitis': 'hep',
             'zoo': 'zoo',
             'breast_cancer_wisconsin': 'bcw'}

#di = list(chain(range(4,10)))

def mat2data(folder):
    names = scipy.io.loadmat(os.path.join(folder, 'database_names.mat'))['Database_Name']
    #mat = scipy.io.loadmat(os.path.join(folder, 'accuracy_v6.mat'))['Complete_Raw_Data_Accuracy']

    mat = scipy.io.loadmat(os.path.join(folder, 'size_v6.mat'))['Complete_Raw_Data_Size']

    data = {}
    print('Here')
    for i in di:
        name = accronyms[names[i].strip()]
        data[name] = {}
        dataset = data[name]
        
        for a, name in enumerate(algos):
            dataset[name] = mat[i][a].tolist()

    return data
    
data = mat2data('/media/bvukobratovic/C06D-C108/data/Doktorat/Results_Greedy_Hereboy/raw/')

import json
with open('cv_data_size.js', 'w') as outfile:
    json.dump(data, outfile)

print(data.keys())
