'''
Created on Mar 31, 2015

@author: Bogdan
'''
from string import Template
import copy
import itertools
import inspect
import operator

bdp_config = {
              'grid':   10
              }

def to_units(num):
#     return "{0}{1}".format(float(int(num)*bdp_config['grid']), "pt")
    return "{0}{1}".format(int(num)*bdp_config['grid'], "pt")

obj_list = []
       
def last():
    return obj_list[-1]

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __getitem__(self, key):
        if key == 0:
            return self.x
        else:
            return self.y
    
    def copy(self):
        return Point(self.x, self.y)
    
    def __str__(self):
        return 'p({0},{1})'.format(self.x,self.y)
    
    def __add__(self, other):
        return Point(self[0] + other[0], self[1] + other[1])
    
    def __sub__(self, other):
        return Point(self[0] - other[0], self[1] - other[1])
    
    def __mul__(self, other):
        return Point(self[0] * other, self[1] * other)
    
#     def resolve(self):
#         try:
#             x = self.x.resolve()
#         except AttributeError:
#             x = self.x
#             
#         try:
#             y = self.y.resolve()
#         except AttributeError:
#             y = self.y
#             
#         return Point(x,y)       
#     
#     @proxy_bioper
#     def __getitem__(self, key):
#         if key == 0:
#             return self.x
#         else:
#             return self.y
#     
#     @proxy_bioper
#     def __add__(self, other):
#         try:
#             x = self.x + other.__getitem__(0, _resolve=True)
#         except AttributeError:
#             x = self.x + other[0]
#             
#         try:
#             y = self.y + other.__getitem__(1, _resolve=True)
#         except AttributeError:
#             y = self.y + other[1]
#             
#         return Point(x,y)

p = Point    

class PosOffset(object):
    
    def resolve(self):
        return Point(self.obj.pos) + Point(self.offset) 
    
    def __init__(self, obj, offset):
        self.obj = obj
        self.offset = offset

class Node(object):
    '''
    classdocs
    '''

    main_settings = ['p', 't', 'size', 'node_sep', 'conn_sep']

    def render_tikz_options(self):
#         size = self.resolve('size')

        options = []
        options.append('draw')
        options.append("minimum width=" + to_units(self.size[0]))
        options.append("minimum height=" + to_units(self.size[1]))
#         
#         size = self.resolve('size')
        
        for s, val in self.settings.items():
            if not s in self.main_settings:
                if val is True:
                    options.append(s)
                else:
                    options.append(s + '=' + str(val))
                    
        return options
        
    def render_tikz(self):
        node_temp = Template("\\node at (${x}, ${y}) [${options}] {$$${text}$$};\n")
        return node_temp.substitute(
                                    x         = to_units(self.p[0] + self.size[0]/2.0),
                                    y         = to_units(self.p[1] - self.size[1]/2.0),
                                    options   = ','.join(self.render_tikz_options()),
                                    text      = self.t
                                    )

    def __call__(self, *args, **kwargs):
#         node = copy.deepcopy(self)
#         for key,value in kwargs.items():
#             setattr(node,key,value)

        kwargs['template'] = self
        
        return Node(*args, **kwargs)

#     @proxy_bioper
    def __getattr__(self, attr):
        try:
            return self.settings[attr]
        except KeyError:
            return getattr(self.template, attr)

#     @proxy_bioper
    def n(self, pos):
#         return PosOffset(self, (pos * self.conn_sep, self.size[1]))
        return self.p + (pos * self.conn_sep, self.size[1])
    
#     @proxy_bioper
    def r(self, pos):
        return self.p + (self.size[0] + pos*self.node_sep[0], 0)
    
#     @proxy_bioper
    def b(self, pos):
        return self.p + (0, self.size[1] + pos*self.node_sep[1])
    
#     def resolve(self, attr):
#         try:
#             attr_val = self.settings[attr]
#             
#             try:
#                 return attr_val.resolve()
#             except AttributeError:
#                 return attr_val
#             
#         except KeyError:
#             return self.template.resolve(attr)
    
    
#     def _get_resolved_settings(self):
#         if self.template is not None:
#             resolved = self.template._get_resolved_settings()
#         else:
#             resolved = {}
#             
#         for key, value in self.settings.items():
#             try:
#                 resolved[key] = value.resolve()
#             except AttributeError:
#                 resolved[key] = value
#             
#         return resolved    
#     
#     def resolve_all(self):
#         self.settings = self._get_resolved_settings()
        
    
#     def mv(self, x=0.0, y=0.0, **kwargs):
#         pos = (self.pos[0] + x, self.pos[1] + y)
#         kwargs["pos"] = pos
#         
#         return self.__call__(**kwargs)
#     
#     def left(self, step=1, **kwargs):
#         node = self.__call__(**kwargs)
#         node.pos = (self.pos[0] - self.size[0] - step*self.node_sep, self.pos[1])
#         
#         return node
#     
#     def right(self, step=1, **kwargs):
#         node = self.__call__(**kwargs)
#         node.pos = (self.pos[0] + self.size[0] + step*self.node_sep, self.pos[1])
#         
#         return node
#    
#     def top(self, step=1, **kwargs):
#         return self.mv(y=-step*self.node_sep, **kwargs)
#     
#     def bottom(self, step=1, **kwargs):
#         return self.mv(y=step*self.node_sep, **kwargs)
#     
#     def at(self, coord):
#         
#         side_pos = int(coord[1:]) * self.conn_sep
#         
#         if (coord[0] == 't'):
#             conn_pos = (self.pos[0] + side_pos, self.pos[1] + self.size[1])
#         elif (coord[0] == 'l'):
#             conn_pos = (self.pos[0], self.pos[1] + self.size[1] - side_pos)
#         elif (coord[0] == 'b'):
#             conn_pos = (self.pos[0] + side_pos, self.pos[1])
#         elif (coord[0] == 'r'):
#             conn_pos = (self.pos[0] + self.size[0], self.pos[1] + self.size[1] - side_pos)
#         
#         return conn_pos

    #def __init__(self, pos=(0, 0), size=(1,1), text="", options=[], node_sep=1, conn_sep=1, shape='rectangle'):
    def __init__(self, p=None, t=None, size=None, template=None, resolve=True, **kwargs):
        '''
        Constructor
        '''
        
        if template is None:
            try:
                template = node
            except NameError:
                pass
            
        self.template = template
        self.settings = kwargs
        
        if p is not None:
            self.settings['p'] = p
            
        if size is not None:
            self.settings['size'] = size
            
        if t is not None:
            self.settings['t'] = t
        
        if template is not None:
            for key, value in self.template.settings.items():
                if not key in self.settings:
                    self.settings[key] = value
        
        if resolve:
#             self.resolve_all()
            obj_list.append(self)
            
            
#             try:
#                 resolved[key] = value.resolve()
#             except AttributeError:
#                 resolved[key] = value
            
       
        
#         try:
#             self.size = size.size
#         except AttributeError:
#             self.size = (size[0], size[1])
#             
#         try:
#             self.pos = pos.pos
#         except AttributeError:
#             self.pos = (pos[0], pos[1])
#             
#         self.text = text
#         self.node_sep = node_sep
#         self.options = options
#         self.conn_sep = conn_sep

origin = p(1000, 1000)

node = Node(
          resolve   = False,
          template  = None,
          p         = origin,
          t         = "",
          size      = p(10, 10),
          node_sep  = p(1,1),
          conn_sep  = 1,
          )

def templ(obj, *args, **kwargs):
    kwargs['resolve'] = False
    
    return obj(*args, **kwargs)

# def node(*args, **kwargs):
            

class Path(object):
    
    def render_tikz_options(self):
        options = []
        
        options.append("draw")
        options.extend(self.options)
        
        return options
    
    def render_tikz_path(self):
        path_iter = itertools.izip_longest(self.path, self.style, fillvalue=self.def_style)
        path_tikz = []
        
        for p in path_iter:
            try:
                path_str = p[0].render_tikz_path()
            except AttributeError:
                path_str = "(" + to_units(p[0][0]) + "," + to_units(p[0][1]) + ")"
                
            path_tikz.append(path_str)
            path_tikz.append(p[1])
            
        return ' '.join(path_tikz[:-1])
    
    def render_tikz(self):
        node_temp = Template("\\path [${options}] ${path};\n")
        
        return node_temp.substitute(
                                    options   = ','.join(self.render_tikz_options()),
                                    path      = self.render_tikz_path()
                                    )
    
    def __init__(self, path=[(0.0, 0.0)], style=[], def_style="-|", options=[]):
        obj_list.append(self)
        
        self.path = path
        self.style = style
        self.def_style = def_style
        self.options = options
        
        