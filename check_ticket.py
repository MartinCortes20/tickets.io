# Uso: python3 check_ticket.py ruta/ticket.py  (simula la impresora y valida el ticket)
import sys,types
class P:
    def __init__(s,*a,**k):pass
    def text(s,t):
        for l in t.split('\n'):
            if len(l)>32: print('LARGO',len(l),repr(l))
    def __getattr__(s,n): return lambda *a,**k:None
m=types.ModuleType('escpos');m2=types.ModuleType('escpos.printer');m2.Usb=P;m2.Dummy=P
sys.modules['escpos']=m;sys.modules['escpos.printer']=m2
import ast
src=open(sys.argv[1]).read()
for n in ast.walk(ast.parse(src)):
    if isinstance(n,ast.Constant) and isinstance(n.value,str) and '\\' in n.value: print('BACKSLASH LITERAL',n.lineno,repr(n.value))
    if isinstance(n,ast.Constant) and n.value in ('TERMINAL: \n','TERMINAL:\n'): print('TERMINAL VACIO',n.lineno)
exec(compile(open(sys.argv[1]).read(),sys.argv[1],'exec'))
