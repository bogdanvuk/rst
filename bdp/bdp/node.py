'''
Created on Mar 31, 2015

@author: Bogdan
'''
from string import Template
import copy
import itertools
import inspect
import operator
# from alias_dict import AliasDict
import subprocess
import math

def to_units(num):
#     return "{0}{1}".format(float(int(num)*bdp_config['grid']), "pt")
    return "{0}{1}".format(num*bdp_config['grid'], "pt")

def from_units(str):
#     return "{0}{1}".format(float(int(num)*bdp_config['grid']), "pt")
    str = str.replace('pt', '')
    return float(str) / bdp_config['grid']

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
        
    def __setitem__(self, key, val):
        if key == 0:
            self.x = val
        else:
            self.y = val
    
    def copy(self):
        return Point(self.x, self.y)
    
    def __str__(self):
        return 'p({0},{1})'.format(self.x,self.y)
    
    __repr__ = __str__
    
    def __add__(self, other):
        return Point(self[0] + other[0], self[1] + other[1])
    
    def __sub__(self, other):
        return Point(self[0] - other[0], self[1] - other[1])
    
    def __mul__(self, other):
        return Point(self[0] * other, self[1] * other)
    
    def __rmul__(self, other):
        return Point(self[0] * other, self[1] * other)
    
#     def resolve(self):
#         try:
#             x = self.x.resolve()
#         except AttributeError:
#             x = self.x
#             
#         try:
#             y = self.y.k()
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

#     main_settings = ['p', 't', 'size',
#                      'node_sep', 'conn_sep',
#                      'border', 'anchor', 'margin']
    
#     __slots__ = ['template', 'settings']
    
    template = None
    settings = None
    def_settings = {}
    aliases = {}
    meta_options = ['template', 'p', 't']

    def options(self, excluded=None):
        if not excluded:
            excluded = set()
        
        excluded |= set(self.meta_options)
        
        for s in self.settings:
            if s not in excluded:
                excluded.add(s)
                yield s
                
        if self.template:
            yield from self.template.options(excluded)
            
        for s in self.def_settings:
            if s not in excluded:
                excluded.add(s)
                yield s
                 

    def render_tikz_options(self):
        options = []
        
        if self.border:
            options.append('draw')
        
        options.append('anchor=north west')
        
#         for s, val in self.settings.items():
#             if not s in self.meta_options:
        for s in self.options():
            val = getattr(self, s)
            try:
                options.append(getattr(self, "render_tikz_" + s)())
            except AttributeError:
                if val is True:
                    options.append(s)
                else:
                    options.append(s + '=' + str(val))
                    
        return ','.join(options)
    
    def render_tikz_p(self):
        pos = self.p + bdp_config['origin_offset']
        return "{0}, {1}".format(to_units(pos[0]), to_units(pos[1]))
    
    def render_tikz_t(self):
        try:
            return self.t
        except AttributeError:
            return ''
    
    def render_tikz(self):
        pos = self.render_tikz_p()
        
        if pos:
            pos = "at ({0})".format(pos)
        
        options = self.render_tikz_options()
        
        if options:
            options = "[{0}]".format(options)
            
        text = self.render_tikz_t()
        
        if text:
            text = "{{{0}}}".format(text)
        else:
            text = "{}"
        
        return ' '.join(["\\node", pos, options, text, ";\n"])

    def __call__(self, *args, **kwargs):
        if (not args) and (not kwargs):
            obj_list.append(self.render_tikz())
            
            return self
        else:
            kwargs['template'] = self
        
            return self.__class__(*args, **kwargs)
        
    def __getattr__(self, attr):
        try:
            return self.settings[attr]
        except (KeyError, TypeError):
            try:
                return getattr(self.template, attr)
            except AttributeError:
                try:
                    return self.def_settings[attr]
                except KeyError:
                    raise AttributeError

    def __setattr__(self, attr, val):
        if hasattr(self.__class__, attr):
            object.__setattr__(self, attr, val)
        else:
            self.settings[attr] = val
        
    def __init__(self, **kwargs):

        try:
            self.template = kwargs['template']
        except KeyError:
            try:
                self.template = node
            except NameError:
                self.template = None
        
        import copy
        self.settings = copy.deepcopy(kwargs)
        
class Block(Node):
    
    meta_options = ['node_sep', 'conn_sep', 'border', 'anchor'] + Node.meta_options
    
    def_settings = {
            'border' :  True,
            'margin' :  p(0.3,0.3),
            'size'   :  p(None, None),
            'p'      :  p(0,0),
            'node_sep' : p(1,1),
            'conn_sep' : 1,
            'align'    : "center"
            }
    
#     def __getattr__(self, attr):
#         return super().__getattr__(attr)
# 
#     def __setattr__(self, attr, val):
#         super().__setattr__(attr, val)
    
    def render_tikz_size(self):
        if self.size:
            return "minimum width=" + to_units(self.size[0]) + "," + "minimum height=" + to_units(self.size[1])
            
    def render_tikz_margin(self):
        if self.margin[0] is not None:
            return "text width=" + to_units(self.size[0] - 2*self.margin[0])
            
        if self.margin[1] is not None:
            return "text height=" + to_units(self.size[1] - 2*self.margin[1])
    
    import subprocess

    @property
    def size(self):
        try:
            size = self.__getattr__('size')
        except AttributeError:
            size = p(None,None)
        
        if (size[0] is None) or (size[1] is None):
        
            if self.t:
                bdp_console_header = '[BDP]'
                tex = ('latex '
                      '"\\documentclass{standalone}'
                      '\\newlength\\mywidth\\newlength\\myheight'
                      '\\begin{document}'
                      '\\settowidth{\\mywidth}{' + self.t + '}'
                      '\\settoheight{\\myheight}{' + self.t + '}'
                      '\\typeout{' + bdp_console_header + '\\the\\mywidth,\\the\\myheight}'
                      '\\end{document}"'
                      ' -draftmode -interaction=nonstopmode')
        
                try:
                    ret = subprocess.check_output(tex, shell=True, universal_newlines=True)
                    for line in ret.split('\n'):
                        if line.startswith(bdp_console_header):
                            line = line.replace(bdp_console_header, '')
                            vals = line.split(',')
                            
                            if size[0] is None:
                                size[0] = math.ceil(from_units(vals[0]) + (2*self.margin[0]))
                                
                                if size[0] == 0:
                                    size[0] = 1
                                
                            if size[1] is None:
                                size[1] = math.ceil(from_units(vals[1]) + (2*self.margin[1]))
                                
                                if size[1] == 0:
                                    size[1] = 1
                                
                            break
                            
                except subprocess.CalledProcessError as e:
                    print ("Ping stdout output:\n", e.output)
                
            else:
                return p(1,1)
            
        return size
        
    @size.setter
    def size(self, value):   
        self.settings['size'] = value
    
    @property
    def p(self):
        pos = self.__getattr__('p')
        
        try:
            anchor = self.anchor
        
            return 2*pos - anchor
        except AttributeError:
            return pos
        
    @p.setter
    def p(self, value):
        self.settings['p'] = value
        
    def n(self, pos):
        return self.p + (pos * self.conn_sep, 0)
    
    def e(self, pos):
        if isinstance( pos, int ):
            return self.p + (self.size[0], pos * self.conn_sep)
        else:
            return self.p + (self.size[0], pos * self.size[1])
    
    def s(self, pos):
        return self.p + (pos * self.conn_sep, self.size[1])
    
    def w(self, pos):
        if isinstance( pos, int ):
            return self.p + (0, pos * self.conn_sep)
        else:        
            return self.p + (0, pos * self.size[1])
    
    def r(self, pos):
        return self.p + (self.size[0] + pos*self.node_sep[0], 0)
    
    def l(self, pos):
        return self.p - (pos*self.node_sep[0], 0)
    
    def b(self, pos):
        return self.p + (0, self.size[1] + pos*self.node_sep[1])
    
    def __init__(self, p=None, t=None, size=None, **kwargs):
        super().__init__(**kwargs)
        
        if p is not None:
            self.p = p
             
        if size is not None:
            self.size = size
             
        if t is not None:
            self.t = t
            
class Path(object):
    
    def render_tikz_options(self):
        options = []
        
        options.append("draw")
        options.extend(self.options)
        
        return options
    
    def render_tikz_path(self):
        path_iter = itertools.zip_longest(self.path, self.style, fillvalue=self.def_style)
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

def templ(obj, *args, **kwargs):
    kwargs['resolve'] = False
    
    return obj(*args, **kwargs)

origin = p(0, 0)

bdp_config = {
              'grid'            : 10,
              'origin_offset'   : p(1000, 1000)
              }

node = Node()
block = Block()

text = block(
            border = False
            )
        