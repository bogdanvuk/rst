dt = { '00': {'class':0,
              'id': 0,
              'level': 0,
              'coef': [0.2, 0.3],
              'thr': 0.25,
              'left': '10',
              'right': '11'},
       '10': {'class':1,
              'id': 0,
              'level': 1,
              'coef': [],
              'thr': 0,
              'left': '',
              'right': ''},
       '11': {'class':0,
              'id': 1,
              'level': 1,
              'coef': [0.2, -0.3],
              'thr': -0.07,
              'left': '21',
              'right': '20'},
       '20': {'class':2,
              'id': 0,
              'level': 2,
              'coef': [],
              'thr': 0,
              'left': '',
              'right': ''},
       '21': {'class':0,
              'id': 1,
              'level': 2,
              'coef': [1, 0],
              'thr': 0.8,
              'left': '30',
              'right': '31'},
       '30': {'class':3,
              'id': 0,
              'level': 3,
              'coef': [],
              'thr': 0,
              'left': '',
              'right': ''},
       '31': {'class':4,
              'id': 1,
              'level': 3,
              'coef': [],
              'thr': 0,
              'left': '',
              'right': ''}


}

import matplotlib.pyplot as plt
import matplotlib
import attrspace_plot
import numpy as np
import math

attr, cls = attrspace_plot.load_arff("../data/vene.csv")
ds = {'attr': attr, 'cls': cls}

attrspace_plot.plot(ds, (0,1), alpha=0.3)

y,x=np.ogrid[0:1:100j,0:1:100j]

matplotlib.rcParams['contour.negative_linestyle'] = 'solid'

def lines_intersection(l1, l2):
    res = np.cross(l1, l2)
    if res[2] == 0:
        return None
    else:
        return np.array([res[0]/res[2], res[1]/res[2]])

axis_coefs = [
    np.array([1, 0, 0]),
    np.array([0, 1, 0]),
    np.array([1, 0, -1]),
    np.array([0, 1, -1])
]

axis_nodes = [
    np.array([0, 0]),
    np.array([0, 1]),
    np.array([1, 0]),
    np.array([1, 1])
]

def trim_outside_intersections(hier, path, intersections):
    rem = []
    for i, inter in enumerate(intersections):
        remove = False
        for a in [0,1]:
            if (inter[a] < 0) or (inter[a] > 1):
                remove = True
                break

        if not remove:
            for h,p in zip(hier, path):
                #print('h{}{}, p={} '.format(h['level'], h['id'], p))
                #print(inter, np.dot(inter, h['coef']) - h['thr'])
                if np.absolute(np.dot(inter, h['coef']) - h['thr']) < 1e-5:
                    continue
                elif ((np.dot(inter, h['coef']) < h['thr']) and (p == 'right')) or \
                     ((np.dot(inter, h['coef']) > h['thr']) and (p == 'left')):
                    remove = True
                    #print('Removed')
                    break

        if remove:
            rem.append(i)

    for i in reversed(rem):
        del intersections[i]


def get_intersections(hier, path, node):
    hcoef = node['coef'] + [-node['thr']]
    intersections = []
    for a in axis_coefs:
        inter = lines_intersection(hcoef, a)
        if inter is not None:
            intersections.append(inter)

    for h in hier:
        phcoef = h['coef'] + [-h['thr']]
        inter = lines_intersection(hcoef, phcoef)
        if inter is not None:
            intersections.append(inter)

    print('{}{}: '.format(node['level'], node['id']))

    trim_outside_intersections(hier, path, intersections)

    print(intersections)
    return intersections

def plot_subspace(dt, n, hier=[], path=[]):
    if n['left']:
        inter = get_intersections(hier, path, n)
        n['line'] = inter
        if hier is None:
            plt.contour(x.ravel(), y.ravel(), n['coef'][0]*x + n['coef'][1]*y, [n['thr']], linewidths=2, colors='k')
        else:
            print(inter)
            plt.plot([inter[0][0], inter[1][0]], [inter[0][1], inter[1][1]], linewidth=2, color='k')

        hier.append(n)
        for ch in ['left', 'right']:
            path.append(ch)
            plot_subspace(dt, dt[n[ch]], hier, path)
            path.pop()

        hier.pop()
    else:
        intersections = []
        intersections.extend(axis_nodes)
        for h in hier:
            intersections.extend(h['line'])

        trim_outside_intersections(hier, path, intersections)
        print('CLASS: {}{}: '.format(n['level'], n['id']))
        print(intersections)

        import jarvis
        intersections = jarvis.convex_hull([i.tolist() for i in intersections])
        import centroids
        center = centroids.calculate_polygon_centroid(intersections + [intersections[0]])

#         center = np.array([0,0])
#         for inter in intersections:
#             center = np.add(center, inter)
# 
#         center = 1/len(intersections)*center

        plt.text(center[0], center[1], 'C' + str(n['class']), size=30)
        print('CLASS: {}{}: '.format(n['level'], n['id']))
        print(intersections)

#print(get_intersections([], dt['00']))

plot_subspace(dt, dt['00'])

# for name, n in dt.items():
#     if n['coef']:
#         plt.contour(x.ravel(), y.ravel(), n['coef'][0]*x + n['coef'][1]*y, [n['thr']], linewidths=2, colors='k')

plt.savefig("dt2plot.pdf")
