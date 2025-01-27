#%%
from dataclasses import dataclass

'''
λx.x
λx.λy.x
'''

abc = 'abcdefghijklmnopqrstuvwxyz'
def numalph(n): return abc[n%26] + str(n//26 or '')

def dedup(x: list): return list(dict.fromkeys(x))

Var = int

ctr = 0
def newVar():
  global ctr
  return (ctr:=ctr+1)

@dataclass(frozen=True)
class Node:
  A:any
  B:any
  def __repr__(self): return s(self)

class Lam(Node):pass
class App(Node):pass

def varlist (node):
  if isinstance(node, Var): return [node]
  return dedup(varlist(node.A) + varlist(node.B))

def repr(node, varmap):
  if isinstance(node, Var): return varmap[node]
  if isinstance(node, Lam): return f'λ{varmap[node.A]}.{repr(node.B, varmap)}'
  if isinstance(node, App): return f'({repr(node.A, varmap)} {repr(node.B, varmap)})'

def s(node):
  varmap = {v: numalph(i) for i, v in enumerate(dedup(varlist(node)))}
  return repr(node, varmap)

def p(*node):
  print(*[s(n) for n in node])
  return node[-1]

def replace(l, a, b):
  if l == a: return b
  if isinstance(l,Node):
    return type(l)(replace(l.A, a, b), replace(l.B, a, b))
  return l

def subst(l, a, b): return l if isinstance(l, Lam) and l.A == a else replace(l, a, b)

def copy(n):
  for x in varlist(n): n = replace(n, x, newVar())
  return n

def step(n):
  if isinstance(n, Lam): return Lam(n.A, step(n.B))
  if isinstance(n, App):
    if isinstance(n.A, Lam): return subst(n.A.B, n.A.A, n.B)
    if isinstance(n.A, App): return App(step(n.A), n.B)
    if isinstance(n.B, App): return App(n.A, step(n.B))
  return n

def eval(n, verbose = True):
  while True:
    if verbose: p(n)
    n2 = step(n)
    if s(n2) == s(n): return n
    n = n2

a,b,c = newVar(), newVar(), newVar()
l1 = Lam(a, a)
T = Lam(a, Lam(b, a))
F = Lam(a, Lam(b, b))

l3 = subst(l1, a, b)
assert l3.A == a

assert varlist(a) == [a]
assert varlist(l1) == [a]
assert varlist(T) == [a,b]

assert s(a) == 'a'
assert s(l1) == 'λa.a'
assert s(T) == 'λa.λb.a'

l2 = replace(l1, a,c)
assert l2.A == c
assert l2.B == c


def reduce(l, f, d):
  for x in l:d = f(d, x)
  return d

def map(l, f): return reduce(l, lambda a,b: a + [f(b)], [])

def cc(*fn): return lambda x: reduce(fn, lambda a,b: b(a), x)

pstep = cc(step,p)

x = App(T,copy(F))

eval(x)

None

#%%

ss = Lam(a, App(a,a))
eval(App(App(ss, T), F),F)