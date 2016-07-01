dt = { '00': {'class':0,
              'id': 0,
              'level': 0,
              'coef': [0.2, 0.3],
              'thr': -0.17,
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
              'thr': 0.17,
              'left': '20',
              'right': '21'},
       '20': {'class':2,
              'id': 0,
              'level': 1,
              'coef': [],
              'thr': 0,
              'left': '',
              'right': ''},
       '21': {'class':3,
              'id': 1,
              'level': 1,
              'coef': [],
              'thr': 0,
              'left': '',
              'right': ''}

}

dot_tmplt = """
digraph foo {{
    edge [dir=none]
    node [fontsize=30]
    nodesep=0.5
    ranksep = "0.5 equally"
    {}
    {}
}}
"""

node_tmplt = '{} [shape={}]'
hier_tmplt = '{} -> {}'

class NodePool(list):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cnt = 0

    def insert(self, name, node):
        self.cnt += 1
        self.append(node)
        node['id'] = self.cnt
        node['name'] = name
        return node

def dt2dot(dt):
    node_pool = NodePool()
    node_pool.insert('00', dt['00'])

    hier = []
    node_def = []

    while node_pool:
        node = node_pool.pop(0)
        print(node)
        if node['left']:
            node_def.append(node_tmplt.format(node['id'], 'circle'))
            for ch in ['left', 'right']:
                child = node_pool.insert(node[ch], dt[node[ch]])
                hier.append(hier_tmplt.format(node['id'], child['id']))
        else:
            node_def.append(node_tmplt.format(node['id'], 'square'))

    return dot_tmplt.format('\n    '.join(node_def), '\n    '.join(hier))

s = dt2dot(dt)

with open('proba.dot', 'w') as fout:
    fout.write(s)
