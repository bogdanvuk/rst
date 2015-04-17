'''
Created on Mar 31, 2015

@author: Bogdan
'''
from string import Template
import copy
import itertools
import inspect
import operator
from alias_dict import AliasDict
import subprocess

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

#     main_settings = ['p', 't', 'size',
#                      'node_sep', 'conn_sep',
#                      'border', 'anchor', 'margin']
    
#     __slots__ = ['template', 'settings']
    
    template = None
    settings = None
    def_settings = {}
    aliases = {}
    meta_options = ['template', 'p', 't', 'resolve']

    def render_tikz_options(self):
        options = []
        
        if self.border:
            options.append('draw')
        
        options.append('anchor=north west')
        
        for s, val in self.settings.items():
            if not s in self.meta_options:
                try:
                    options.append(getattr(self, "render_tikz_" + s)())
                except AttributeError:
                    if val is True:
                        options.append(s)
                    else:
                        options.append(s + '=' + str(val))
                    
        return ','.join(options)
    
    def render_tikz_p(self):
        return "{0}, {1}".format(to_units(self.p[0]), to_units(self.p[1]))
    
    def render_tikz_t(self):
        return self.t
    
    def render_tikz(self):
        pos = self.render_tikz_p()
        
        if pos:
            pos = "at ({0})".format(pos)
        
        options = self.render_tikz_options()
        
        if options:
            options = "[{0}]".format(options)
            
        text = self.render_tikz_t()
        
        if text:
            text = "{{${0}$}}".format(text)
        else:
            text = "{}"
        
        return ' '.join(["\\node", pos, options, text, ";\n"])

    def __call__(self, *args, **kwargs):
        kwargs['template'] = self
        
        return self.__class__(*args, **kwargs)

    def __getattr__(self, attr):
        try:
            return self.settings[attr]
        except KeyError:
            return getattr(self.template, attr)

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
        
        self.settings = AliasDict()
        
        for k,v in self.aliases.items():
            for alias in v:
                self.settings.alias(k, alias)
        
        self.settings.update(self.def_settings.copy())
        self.settings.update(kwargs)
        
#         if p is not None:
#             self.settings['p'] = p
#             
#         if size is not None:
#             self.settings['size'] = size
#             
#         if t is not None:
#             self.settings['t'] = t
#         
#         self.settings['border'] = border
        
        if self.template is not None:
            for key, value in self.template.settings.items():
                if not key in self.settings:
                    self.settings[key] = value
        
        if self.resolve:
            obj_list.append(self)

class Block(Node):
    
    meta_options = ['node_sep', 'conn_sep', 'border'] + Node.meta_options
    
    def_settings = {
            'resolve':  True,
            'border' :  True,
            'margin' :  p(5,None)
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
            return "text width=" + to_units(self.size[0] - (2*self.margin[0])/bdp_config['grid'])
            
        if self.margin[1] is not None:
            return "text height=" + to_units(self.size[1] - (2*self.margin[0])/bdp_config['grid'])
    
    import subprocess

    @property
    def size(self):
        
        tex = r"""
\documentclass{article}
\newlength\mylength
\begin{document}
\settowidth{\mylength}{\raggedright The quick brown fox jumps over the lazy dog}
\typeout{\the\mylength}
\end{document}
"""        

        
#         tex = r'"\documentclass{standalone}\newlength\mylength\begin{document}\settowidth{\mylength}{\raggedright The quick brown fox jumps over the lazy dog}\typeout{\the\mylength}\end{document}"'
#         tex = '"\\documentclass{standalone}\\newlength\\mylength\\begin{document}\\settowidth{\\mylength}{\\raggedright The quick brown fox jumps over the lazy dog}\\typeout{\\the\\mylength}\\end{document}"'
        tex = '"\\documentclass{standalone}\\newlength\\mylength\\begin{document}\\settowidth{\\mylength}{The quick brown fox jumps over the lazy dog}\\typeout{\\the\\mylength}\\end{document}"'
        print(tex)
        
#         try:
#             print("ev")
#         ret = subprocess.check_output('latex "\\documentclass{standalone}\\newlength\\mylength\\begin{document}\\settowidth{\\mylength}{\\raggedright The quick brown fox jumps over the lazy dog}\\typeout{\\the\\mylength}\\end{document}" -draftmode -interaction=nonstopmode', shell=True)
# #             ret = subprocess.check_output(["latex", tex, "-draftmode", "-interaction=nonstopmode"], shell=True)
#         except:
#             print("here?")
        
#         if super().size is None:
        try:
            ret = subprocess.check_output('latex "\\documentclass{standalone}\\newlength\\mylength\\begin{document}\\settowidth{\\mylength}{Proba}\\typeout{\\the\\mylength}\\end{document}" -draftmode -interaction=nonstopmode', shell=True, universal_newlines=True)
#             ret = subprocess.check_output(["latex", tex, "-draftmode", "-interaction=nonstopmode"])
#             print("here?")
            print(ret)
        except subprocess.CalledProcessError as e:
            print ("Ping stdout output:\n", e.output)
            
#         print(ret)
#         else:
#             return super().size
        
    @size.setter
    def size(self, value):   
        self.settings['size'] = value
    
    @property
    def p(self):
        if 'anchor' in self.settings:
            return 2*self.settings['p'] - self.settings['anchor']
        else:
            return self.settings['p']
        
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
    
    def __init__(self, p=None, t=None, size=None, border=True, **kwargs):
        super().__init__(**kwargs)
        
        if p is not None:
            self.p = p
             
        if size is not None:
            self.size = size
             
        if t is not None:
            self.t = t
         
        self.border = border
            
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

origin = p(1000, 1000)

node = Node(
          resolve   = False,
          template  = None,
          p         = origin,
          t         = "",
          size      = p(10, 10),
          node_sep  = p(1,1),
          conn_sep  = 1,
          align     = "center"
          )

block = Block(
          resolve   = False,
          template  = None,
          p         = origin,
          t         = "",
#           size      = p(10, 10),
          node_sep  = p(1,1),
          conn_sep  = 1,
          align     = "center"
          )

class Text(Node):
    
    def __init__(self, text, **kwargs):
        if 'border' not in kwargs:
            kwargs['border'] = False
            
        if 'size' not in kwargs:
            kwargs['size'] = p(0,0)
        
        kwargs['t'] = text
        
        super().__init__(**kwargs)
        