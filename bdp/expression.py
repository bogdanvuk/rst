'''
Created on Apr 3, 2015

@author: bvukobratovic
'''

def proxy_bioper(method):
    def wrapper(self, other, _resolve=False):
        if not _resolve:
            return Expression(self, method.__name__, other)
        else:
            try:
                other = other.resolve()
            except AttributeError:
                pass
            
            return method(self, other)
    return wrapper  

# def proxy_unoper(method):
#     def wrapper(self):
#         if simarch_inst():
#             return Expression(self, method.__name__)
#         else:
#             return method(self)
#     return wrapper  

class _ExpressionBase(object):
    """Base class for all interfaces and sliced interfaces."""
    
    def __init__(self):
        pass
    
    @proxy_bioper
    def __getattr__(self, name):
        return getattr(self.settings[name].resolve())
#        return getattr(self.read(), name)
    
    def __nonzero__(self):
        if self.read():
            return 1
        else:
            return 0

    # length
    def __len__(self):
        return len(self.read())

    def __bool__(self):
        return bool(self.read())

        
    # integer-like methods

# #     @proxy_bioper
#     def __contains__(self, other):
#         return self.read() in other
# 
#     @proxy_bioper
#     def __add__(self, other):
#         return self.read() + other
#     
#     @proxy_bioper
#     def __ilshift__(self, other):
#         self.s_con(other)
#         return self
#     
#     @proxy_bioper
#     def __irshift__(self, other):
#         self.connect(other, side=IntfDir.master)
#         return self
#     
#     @proxy_bioper
#     def __radd__(self, other):
#         return other + self.read()
# 
#     @proxy_bioper    
#     def __sub__(self, other):
#         return self.read() - other
#     @proxy_bioper
#     def __rsub__(self, other):
#         return other - self.read()
# 
#     @proxy_bioper
#     def __mul__(self, other):
#         return self.read() * other
#     @proxy_bioper
#     def __rmul__(self, other):
#         return other * self.read()
# 
#     @proxy_bioper
#     def __div__(self, other):
#         return self.read() / other
#     @proxy_bioper
#     def __rdiv__(self, other):
#         return other / self.read()
# 
#     @proxy_bioper    
#     def __truediv__(self, other):
#         return self.read().__truediv__(other)
#     @proxy_bioper
#     def __rtruediv__(self, other):
#         return other.__truediv__(self.read())
#     
#     @proxy_bioper
#     def __floordiv__(self, other):
#         return self.read() // other
#     @proxy_bioper
#     def __rfloordiv__(self, other):
#         return other //  self.read()
# 
#     @proxy_bioper    
#     def __mod__(self, other):
#         return self.read() % other
#     @proxy_bioper
#     def __rmod__(self, other):
#         return other % self.read()
# 
#     # XXX divmod
# 
#     @proxy_bioper    
#     def __pow__(self, other):
#         return self.read() ** other
#     def __rpow__(self, other):
#         return other ** self.read()
# 
#     @proxy_bioper
#     def __lshift__(self, other):
#         return self.read() << other
#     @proxy_bioper
#     def __rlshift__(self, other):
#         return other << self.read()
# 
#     @proxy_bioper            
#     def __rshift__(self, other):
#         return self.read() >> other
#     @proxy_bioper
#     def __rrshift__(self, other):
#         return other >> self.read()
# 
#     @proxy_bioper           
#     def __and__(self, other):
#         return self.read() & other
#     @proxy_bioper
#     def __rand__(self, other):
#         return other & self.read()
# 
#     @proxy_bioper
#     def __or__(self, other):
#         return self.read() | other
#     @proxy_bioper
#     def __ror__(self, other):
#         return other | self.read()
#     
#     @proxy_bioper
#     def __xor__(self, other):
#         return self.read() ^ other
#     @proxy_bioper
#     def __rxor__(self, other):
#         return other ^ self.read()
#     @proxy_unoper
#     def __neg__(self):
#         return -self.read()
#     @proxy_unoper
#     def __pos__(self):
#         return +self.read()
#     @proxy_unoper
#     def __abs__(self):
#         return abs(self.read())
#     @proxy_unoper
#     def __invert__(self):
#         return ~self.read()
#         
#     # conversions
#     @proxy_unoper
#     def __int__(self):
#         return int(self.read())
#     @proxy_unoper
#     def __float__(self):
#         return float(self.read())
#     @proxy_unoper
#     def __oct__(self):
#         return oct(self.read())
#     @proxy_unoper
#     def __hex__(self):
#         return hex(self.read())
#     @proxy_unoper
#     def __index__(self):
#         return int(self.read())
#     # comparisons
#     @proxy_bioper
#     def __eq__(self, other):
# #         try:
# #             other = other.read()
# #         except AttributeError:
# #             pass
#         return self.read() == other
#     
#     @proxy_bioper
#     def __ne__(self, other):
#         return self.read() != other 
#     @proxy_bioper
#     def __lt__(self, other):
#         return self.read() < other
#     @proxy_bioper
#     def __le__(self, other):
#         return self.read() <= other
#     @proxy_bioper
#     def __gt__(self, other):
#         return self.read() > other
#     @proxy_bioper
#     def __ge__(self, other):
#         return self.read() >= other

class Expression(_ExpressionBase):
   
    def __init__(self, elem, oper, *args, **kwargs):
#         _ExpressionBase.__init__(self, parent=None, name=None)
        _ExpressionBase.__init__(self)
        
        self.args = [elem] + list(args)
        self.kwargs = kwargs
        self.oper = oper

    def _replace(self, elem, key):
        if isinstance(key, int):
            self.args[key] = elem
        elif isinstance(key, str):
            self.kwargs[key] = elem

    def resolve(self):
        args = []
        
        for a in self.args[1:]:
            try:
                args.append(a.resolve())
            except AttributeError:
                try:
                    args.append(a.eval())
                except AttributeError:
                    args.append(a)
                
        kwargs = {}
        
        for k,v in self.kwargs.items():
            try:
                kwargs[k] = v.resolve()
            except AttributeError:
                try:
                    kwargs[k] = v.eval()
                except AttributeError:
                    kwargs[k] = v
                
        try:
            elem = self.args[0].resolve()
        except (AttributeError, TypeError):
            try:
                elem = self.args[0].eval()
            except AttributeError:
                elem = self.args[0]
                
        kwargs['_resolve'] = True
        try:
            return getattr(elem, self.oper)(*args, **kwargs)
        except TypeError:
            del kwargs['_resolve']
            return getattr(elem, self.oper)(*args)
    
    @proxy_bioper
    def __add__(self, other):
        return Expression(self, '__add__', other)
    
    @proxy_bioper
    def __mul__(self, other):
        return Expression(self, '__mul__', other)
    
    @proxy_bioper
    def __rmul__(self, other):
        return Expression(self, '__rmul__', other)
    